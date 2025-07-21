# 导入包
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 配置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ================== 配置参数 ==================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
batch_size = 32
lr = 0.001
epochs = 50
patience = 10  # 早停容忍轮数
model_save_path = 'model1.pth'

# ================== 数据加载 ==================
data_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

train_dataset = ImageFolder(root="宝石分类/archive_train", transform=data_transform)
test_dataset = ImageFolder(root="宝石分类/archive_test", transform=data_transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# ================== 模型定义 ==================
class CNNModel(nn.Module):
    def __init__(self, num_classes):
        super(CNNModel, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 16 * 16, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

num_classes = len(train_dataset.classes)
model = CNNModel(num_classes).to(device)

# ================== 损失函数与优化器 ==================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)  # 学习率衰减

# ================== 早停初始化 ==================
best_accuracy = 0
no_improve_epochs = 0

# ================== 训练 ==================
train_losses = []
test_accuracies = []
start_time = time.time()

for epoch in range(epochs):
    model.train()
    total_loss = 0
    progress_bar = tqdm(train_loader, desc=f"第 {epoch + 1} 轮训练")

    for images, labels in progress_bar:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        progress_bar.set_postfix({"loss": loss.item()})

    avg_loss = total_loss / len(train_loader)
    train_losses.append(avg_loss)

    # ================== 验证 ==================
    model.eval()
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    accuracy = 100 * correct / total
    test_accuracies.append(accuracy)
    print(f"第 {epoch + 1} 轮: 平均损失={avg_loss:.4f}, 测试准确率={accuracy:.2f}%")

    # 学习率调整
    scheduler.step()

    # 早停判断
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        no_improve_epochs = 0
        torch.save(model.state_dict(), model_save_path)
    else:
        no_improve_epochs += 1
        if no_improve_epochs >= patience:
            print(f"早停：连续 {patience} 轮无提升，提前结束训练")
            break

end_time = time.time()

# ================== 可视化 ==================
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(train_losses) + 1), train_losses, label="训练损失")
plt.xlabel("轮次")
plt.ylabel("损失")
plt.title("训练损失曲线")
plt.legend()
plt.savefig("Loss1.jpg")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(range(1, len(test_accuracies) + 1), test_accuracies, label="测试准确率", color='orange')
plt.xlabel("轮次")
plt.ylabel("准确率 (%)")
plt.title("测试准确率曲线")
plt.legend()
plt.savefig("Accuracy1.jpg")
plt.close()

# ================== 混淆矩阵可视化 ==================
cm = confusion_matrix(all_labels, all_preds, labels=list(range(num_classes)))
fig, ax = plt.subplots(figsize=(10, 10))
ConfusionMatrixDisplay(cm, display_labels=train_dataset.classes).plot(ax=ax, cmap="Blues", colorbar=False)
plt.title("测试集混淆矩阵")
plt.savefig("ConfusionMatrix1.jpg")
plt.close()

# ================== 输出结果 ==================
print(f"训练完成，总耗时：{end_time - start_time:.2f} 秒")
print(f"最佳测试准确率：{best_accuracy:.2f}% (模型已保存)")
