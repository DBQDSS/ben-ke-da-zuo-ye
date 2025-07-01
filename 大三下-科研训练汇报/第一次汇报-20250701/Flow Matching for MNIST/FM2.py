import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torchdiffeq import odeint
import os
from tqdm import tqdm  # 导入 tqdm 库
import matplotlib.pyplot as plt

# 配置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# ================== 配置参数 ==================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
image_size = 28
channels = 1
batch_size = 256
lr = 1e-4
epochs = 100
num_classes = 10
model_save_path = 'FMmodel.pth'
# ================== 数据加载 ==================

# 标准化图片至[-1,1]
def normalize_img(x):
    return 2 * x - 1

transform = transforms.Compose([
    transforms.ToTensor(),              # 将图片转为张量
    transforms.Lambda(normalize_img)    # 调用归一化函数
])
# ================== 模型架构 ==================
class ConditionedDoubleConv(nn.Module):
    """带条件注入的双卷积模块"""

    def __init__(self, in_channels, out_channels, cond_dim):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.norm1 = nn.GroupNorm(8, out_channels)
        self.conv2 = nn.Conv2d(out_channels + cond_dim, out_channels, kernel_size=3, padding=1)
        self.norm2 = nn.GroupNorm(8, out_channels)

    def forward(self, x, cond):
        x = F.silu(self.norm1(self.conv1(x)))
        cond = cond.expand(-1, -1, x.size(2), x.size(3))  # 动态广播条件
        x = torch.cat([x, cond], dim=1)
        return F.silu(self.norm2(self.conv2(x)))


class Down(nn.Module):
    """下采样模块"""

    def __init__(self, in_channels, out_channels, cond_dim):
        super().__init__()
        self.maxpool = nn.MaxPool2d(2)
        self.conv = ConditionedDoubleConv(in_channels, out_channels, cond_dim)

    def forward(self, x, cond):
        x = self.maxpool(x)
        return self.conv(x, cond)


class Up(nn.Module):
    """上采样模块"""

    def __init__(self, in_channels, out_channels, cond_dim):
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv = ConditionedDoubleConv(in_channels, out_channels, cond_dim)

    def forward(self, x1, x2, cond):
        x1 = self.up(x1)
        # 尺寸对齐
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]
        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x, cond)


class ConditionalUNet(nn.Module):
    """维度安全的条件生成UNet"""

    def __init__(self):
        super().__init__()
        # 统一条件编码维度
        self.t_dim = 16
        self.label_dim = 16
        self.cond_dim = self.t_dim + self.label_dim  # 32

        # 时间嵌入
        self.time_embed = nn.Sequential(
            nn.Linear(1, 32),
            nn.SiLU(),
            nn.Linear(32, self.t_dim)
        )
        # 标签嵌入
        self.label_embed = nn.Embedding(num_classes, self.label_dim)

        # 编码路径
        self.inc = ConditionedDoubleConv(1, 64, self.cond_dim)
        self.down1 = Down(64, 128, self.cond_dim)
        self.down2 = Down(128, 256, self.cond_dim)

        # 解码路径
        self.up1 = Up(256 + 128, 128, self.cond_dim)  # 输入通道修正
        self.up2 = Up(128 + 64, 64, self.cond_dim)
        self.outc = nn.Conv2d(64, 1, kernel_size=1)

    def forward(self, x, t, labels):
        # 条件编码 (统一维度)
        t_emb = self.time_embed(t.view(-1, 1))  # [B, 16]
        lbl_emb = self.label_embed(labels)  # [B, 16]
        cond = torch.cat([t_emb, lbl_emb], dim=1)  # [B, 32]
        cond = cond.unsqueeze(-1).unsqueeze(-1)  # [B, 32, 1, 1]

        # 编码器
        x1 = self.inc(x, cond)
        x2 = self.down1(x1, cond)
        x3 = self.down2(x2, cond)

        # 解码器
        x = self.up1(x3, x2, cond)
        x = self.up2(x, x1, cond)
        return self.outc(x)


# ================== 训练与生成 ==================
# 在这里初始化模型和优化器，以便全局访问（特别是generate_with_label）
model = ConditionalUNet().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=lr)


@torch.no_grad()
def generate_with_label(label, num_samples=16):
    """
    生成指定标签的样本。
    Args:
        label (int): 要生成的数字标签 (0-9)。
        num_samples (int): 要生成的样本数量。
    Returns:
        torch.Tensor: 生成的图像张量，形状为 (num_samples, image_size, image_size)，值在 [0, 1] 之间。
    """
    # 保存当前模型的训练状态，设置为评估模式
    current_model_state = model.training
    model.eval()

    # 创建初始噪声和标签张量
    x0 = torch.randn(num_samples, 1, image_size, image_size, device=device)
    labels = torch.full((num_samples,), label, device=device, dtype=torch.long)

    # ODE : t 为时间，x 为当前状态
    def ode_func(t: torch.Tensor, x: torch.Tensor):
        t_expanded = t.expand(x.size(0))  # [1] -> [num_samples]
        vt = model(x, t_expanded, labels) # 预测速度场
        return vt

    # 时间点 : 0 -> 1
    t_eval = torch.tensor([0.0, 1.0], device=device)

    # 解ODE（自适应步长）
    generated = odeint(
        ode_func,
        x0,
        t_eval,
        rtol=1e-5,
        atol=1e-5,
        method='dopri5'
    )

    # 训练状态
    model.train(current_model_state)

    # 后处理
    images = (generated[-1].clamp(-1, 1) + 1) / 2  # [-1,1] -> [0,1]
    return images.cpu().squeeze(1)


def visualize_train(epoch):
    """
    调用目前的model，绘制一个10*10的图片：
    在1-10列分别为每个数字(0-9)生成10张图，在每列第一行添加标签。
    """
    print("生成训练过程中的可视化示例...")
    plt.figure(figsize=(10, 10))
    plt.subplots_adjust(wspace=0.05, hspace=0.05)  # 减少子图间距

    # 为每个数字0-9生成10张图
    for label in range(num_classes):
        # 生成当前数字的10个样本
        generated_images = generate_with_label(
            label=label,
            num_samples=10
        ).numpy()  # 形状 (10, 28, 28)

        # 在当前列绘制，确保每一列代表一个数字
        for i in range(10):
            # 子图位置计算：(行索引 * 总列数) + 列索引 + 1
            # 这里我们希望第0列是数字0的图片，第1列是数字1的图片...
            # 所以是 (行 i * num_classes (10)) + 列 label + 1
            ax = plt.subplot(10, num_classes, (i * num_classes) + label + 1)
            plt.imshow(generated_images[i], cmap='gray', vmin=0, vmax=1)
            ax.axis('off')
            # 在每列的第一行（即 i == 0 时）添加数字标签
            if i == 0:
                ax.set_title(str(label), fontsize=16, pad=5)  # 使用set_title更合适
    plt.suptitle("训练过程中的生成样本", fontsize=20, y=0.97)
    plt.savefig(f"epoch{epoch}.jpg")
    plt.close()


def hundred_image(model_path=model_save_path, num_sample=5):
    print(f"正在从 {model_path} 加载模型并生成{num_sample}张图片...")
    # 创建一个新的模型实例并加载权重
    global model
    original_model = model  # 保存原始模型引用

    loaded_model = ConditionalUNet().to(device)
    if os.path.exists(model_path):
        loaded_model.load_state_dict(torch.load(model_path, map_location=device))
        loaded_model.eval()  # 评估模式
    else:
        print(f"错误: 模型文件未找到: {model_path}。无法生成图片。")
        return

    model = loaded_model  # 临时将全局模型替换为加载的模型

    for k in range(num_sample):
        plt.figure(figsize=(10, 10))
        plt.subplots_adjust(wspace=0.05, hspace=0.05)

        print(f"正在生成第{k + 1}张图...")
        for label in tqdm(range(num_classes), desc="Generating images for each digit"):
            # 生成当前数字的10个样本
            generated_images = generate_with_label(
                label=label,
                num_samples=10
            ).numpy()  # 形状 (10, 28, 28)

            # 在当前列绘制
            for i in range(10):
                ax = plt.subplot(10, num_classes, (i * num_classes) + label + 1)
                plt.imshow(generated_images[i], cmap='gray', vmin=0, vmax=1)
                ax.axis('off')
                # 在每列第一行添加标签
                if i == 0:
                    ax.set_title(str(label), fontsize=16, pad=5)

        plt.suptitle(f"最终生成样本 (第{k + 1}次生成)", fontsize=20, y=0.97)
        plt.savefig(f"generated_image{k + 1}.jpg")
        print(f"生成的图片已保存至: generated_image{k + 1}.jpg")
        plt.close()

    # 恢复全局模型引用
    model = original_model


def train(num_epochs = 100):
    """训练循环"""
    print("开始训练...")
    # 确保 train_loader 在这里是可用的，因为它在 if __name__ == "__main__": 块中初始化
    global train_loader

    for epoch in range(num_epochs):
        # 使用tqdm显示训练进度条
        progress_bar = tqdm(train_loader, desc=f"第 {epoch + 1} 轮训练")
        model.train()  # 训练模式
        total_loss = 0

        for images, labels in progress_bar:  # 添加进度条
            images = images.to(device)
            labels = labels.to(device)

            # 动态噪声生成
            noise = torch.randn_like(images)
            t = torch.rand(images.size(0), device=device)
            # Flow Matching的目标速度是从噪声x0到真实数据x1的速度场
            # x_t = (1-t) * x0 + t * x1
            xt = (1 - t.view(-1, 1, 1, 1)) * noise + t.view(-1, 1, 1, 1) * images

            # 前向计算，模型预测的是速度场 v_t
            vt_pred = model(xt, t, labels)
            # 真实的速度场 v_t = x1 - x0
            loss = F.mse_loss(vt_pred, images - noise)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # 梯度裁剪防止爆炸
            optimizer.step()

            total_loss += loss.item()

            # 更新进度条显示损失
            progress_bar.set_postfix({"损失": f"{total_loss:.4f}"})

        # 每10个epoch生成示例
        if (epoch + 1) % 10 == 0:
            visualize_train(epoch + 1)
        # 对第1个epoch生成示例
        if epoch == 0:
            visualize_train(epoch + 1)

    # 训练结束后保存模型
    torch.save(model.state_dict(), model_save_path)
    print(f"训练完成。模型已保存至: {model_save_path}")


if __name__ == "__main__":
    train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              num_workers=2)
    # 调用现成模型时注释掉即可
    # train(epochs)
    hundred_image(model_save_path)