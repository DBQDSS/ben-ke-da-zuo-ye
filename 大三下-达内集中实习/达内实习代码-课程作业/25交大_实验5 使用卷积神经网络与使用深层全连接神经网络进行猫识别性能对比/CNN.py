import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt
import h5py  # 用于读取 h5 文件
import time
import random
from torchvision import transforms
from tqdm import tqdm  # 导入tqdm模块用于进度条显示

# 设置随机种子，保证结果可复现
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)

# 设置设备（自动检测CUDA）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 数据加载和预处理
def load_data(train_path, test_path):
    """加载猫识别数据集"""
    print(f"Loading data from {train_path} and {test_path}...")

    # 加载训练数据
    train_dataset = h5py.File(train_path, "r")
    train_images = np.array(train_dataset["train_set_x"][:])
    train_labels = np.array(train_dataset["train_set_y"][:])

    # 加载测试数据
    test_dataset = h5py.File(test_path, "r")
    test_images = np.array(test_dataset["test_set_x"][:])
    test_labels = np.array(test_dataset["test_set_y"][:])

    # 调整标签维度
    train_labels = train_labels.reshape((1, train_labels.shape[0])).T
    test_labels = test_labels.reshape((1, test_labels.shape[0])).T

    # 数据预处理
    train_images = train_images.transpose(0, 3, 1, 2)  # 调整维度为 [样本数, 通道数, 高度, 宽度]
    test_images = test_images.transpose(0, 3, 1, 2)

    # 转换为PyTorch张量
    train_images = torch.FloatTensor(train_images)
    train_labels = torch.FloatTensor(train_labels)
    test_images = torch.FloatTensor(test_images)
    test_labels = torch.FloatTensor(test_labels)

    return train_images, train_labels, test_images, test_labels


# 数据增强和转换
def get_transforms(is_train=True):
    """定义数据转换和增强策略"""
    if is_train:
        return transforms.Compose([
            transforms.ToPILImage(),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.RandomResizedCrop(64, scale=(0.8, 1.0)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
    else:
        return transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])


# 定义CNN模型
class CatCNN(nn.Module):
    """猫识别CNN模型"""

    def __init__(self):
        super(CatCNN, self).__init__()
        # 卷积层
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)  # 输入通道3，输出通道16
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64)

        # 池化层
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 8 * 8, 512)
        self.dropout = nn.Dropout(0.5)  # 正则化，防止过拟合
        self.fc2 = nn.Linear(512, 1)

        # 激活函数
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 卷积块1
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool(x)  # 32x32

        # 卷积块2
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)  # 16x16

        # 卷积块3
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.pool(x)  # 8x8

        # 展平
        x = x.view(-1, 64 * 8 * 8)

        # 全连接层
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc2(x))

        return x


# 训练模型
def train_model(model, train_loader, test_loader, criterion, optimizer, epochs, device):
    """训练CNN模型"""
    model.to(device)
    train_losses = []
    test_losses = []
    train_accuracies = []
    test_accuracies = []
    best_accuracy = 0.0
    start_time = time.time()

    # 学习率调度器
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5, verbose=True)

    for epoch in range(epochs):
        # 训练阶段
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0

        # 美化进度条
        progress_bar = tqdm(enumerate(train_loader), total=len(train_loader),
                            desc=f"Epoch {epoch + 1}/{epochs} [Train]", leave=False,
                            bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}")

        for batch_idx, (inputs, labels) in progress_bar:
            inputs, labels = inputs.to(device), labels.to(device)

            # 前向传播
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # L2正则化
            l2_lambda = 0.0001
            l2_reg = 0
            for param in model.parameters():
                l2_reg += torch.norm(param, 2)
            loss += l2_lambda * l2_reg

            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            predicted = (outputs > 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            # 更新进度条信息
            progress_bar.set_postfix({
                'loss': f'{train_loss / (batch_idx + 1):.4f}',
                'acc': f'{100 * correct / total:.2f}%',
                'lr': optimizer.param_groups[0]['lr']
            })

        # 计算训练准确率和损失
        train_accuracy = 100 * correct / total
        avg_train_loss = train_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        train_accuracies.append(train_accuracy)

        # 评估阶段
        test_loss, test_accuracy = evaluate_model(model, test_loader, criterion, device)
        test_losses.append(test_loss)
        test_accuracies.append(test_accuracy)

        # 更新学习率
        scheduler.step(test_loss)

        # 打印本轮训练结果
        print(f'Epoch {epoch + 1}/{epochs}, '
              f'Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.2f}%, '
              f'Test Loss: {test_loss:.4f}, Test Acc: {test_accuracy:.2f}%')

        # 保存最佳模型
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            torch.save(model.state_dict(), 'model1.pth')
            print(f"Best model saved with accuracy: {best_accuracy:.2f}%")

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Training completed in {total_time:.2f} seconds')

    return {
        'train_losses': train_losses,
        'test_losses': test_losses,
        'train_accuracies': train_accuracies,
        'test_accuracies': test_accuracies,
        'total_time': total_time,
        'best_accuracy': best_accuracy
    }


# 评估模型
def evaluate_model(model, data_loader, criterion, device):
    """评估模型性能"""
    model.eval()
    loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        # 美化进度条
        progress_bar = tqdm(enumerate(data_loader), total=len(data_loader),
                            desc="Evaluating", leave=False,
                            bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}")

        for batch_idx, (inputs, labels) in progress_bar:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss += criterion(outputs, labels).item()
            predicted = (outputs > 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            # 更新进度条信息
            progress_bar.set_postfix({
                'loss': f'{loss / (batch_idx + 1):.4f}',
                'acc': f'{100 * correct / total:.2f}%'
            })

    accuracy = 100 * correct / total
    return loss / len(data_loader), accuracy


# 可视化训练结果
def visualize_results(results):
    """可视化训练过程中的损失和准确率"""
    # 绘制训练损失图
    plt.figure(figsize=(10, 6))
    plt.plot(results['train_losses'], label='Train Loss', color='blue', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('Training Loss', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('Training_Loss1.jpg', dpi=300)
    plt.close()

    # 绘制训练和测试准确率图
    plt.figure(figsize=(10, 6))
    plt.plot(results['train_accuracies'], label='Train Accuracy', color='green', linewidth=2)
    plt.plot(results['test_accuracies'], label='Test Accuracy', color='red', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.title('Training and Test Accuracy', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('Training_and_Test_Accuracy1.jpg', dpi=300)
    plt.close()

    print("Visualization saved as 'Training_Loss1.jpg' and 'Training_and_Test_Accuracy1.jpg'")


# 主函数
def main():
    # 数据加载
    train_images, train_labels, test_images, test_labels = load_data('catvnoncat/train.h5', 'catvnoncat/test.h5')

    # 数据转换
    train_transform = get_transforms(is_train=True)
    test_transform = get_transforms(is_train=False)

    # 应用转换
    transformed_train_images = torch.stack([train_transform(img.numpy().transpose(1, 2, 0)) for img in train_images])
    transformed_test_images = torch.stack([test_transform(img.numpy().transpose(1, 2, 0)) for img in test_images])

    # 创建数据加载器
    batch_size = 32
    train_dataset = TensorDataset(transformed_train_images, train_labels)
    test_dataset = TensorDataset(transformed_test_images, test_labels)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # 模型、损失函数和优化器
    model = CatCNN()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 训练模型
    epochs = 50
    results = train_model(model, train_loader, test_loader, criterion, optimizer, epochs, device)

    # 可视化结果
    visualize_results(results)

    # 加载最佳模型
    best_model = CatCNN()
    best_model.load_state_dict(torch.load('model1.pth'))
    best_model.to(device)

    # 最终评估
    test_loss, test_accuracy = evaluate_model(best_model, test_loader, criterion, device)
    print(f'Final Test Accuracy: {test_accuracy:.2f}%')

    # 计算模型参数数量
    total_params = sum(p.numel() for p in best_model.parameters())
    print(f'Number of parameters: {total_params:,}')

    # 输出模型运行总时间
    print(f'Total training time: {results["total_time"]:.2f} seconds')


if __name__ == '__main__':
    main()