# anime_classifier_local.py
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ----------------------
# 本地配置参数 (需根据实际情况修改)
# ----------------------
config = {
    "data_dir": "./archive/Data",  # 数据集路径（需自行下载）
    "batch_size": 16,
    "image_size": 224,  # 匹配ResNet输入尺寸
    "num_epochs": 15,
    "lr": 0.001,
    "num_classes": 5  # 根据实际类别数修改（示例使用5个角色）
}


# ----------------------
# 数据集准备（替换Kaggle的数据读取方式）
# ----------------------
class AnimeDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label


def prepare_dataloaders():
    # 本地数据组织示例结构：
    # ./onepiece_dataset/
    #   ├── luffy/
    #   ├── zoro/
    #   ├── nami/
    #   └── ...

    all_image_paths = []
    labels = []
    class_names = sorted(os.listdir(config["data_dir"]))

    for label, class_name in enumerate(class_names):
        class_dir = os.path.join(config["data_dir"], class_name)
        for img_file in os.listdir(class_dir):
            if img_file.endswith(('.jpg', '.png')):
                all_image_paths.append(os.path.join(class_dir, img_file))
                labels.append(label)

    # 划分训练集/验证集（8:2比例）
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        all_image_paths, labels, test_size=0.2, random_state=42
    )

    # 数据增强配置
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(config["image_size"]),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(config["image_size"]),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    train_dataset = AnimeDataset(train_paths, train_labels, train_transform)
    val_dataset = AnimeDataset(val_paths, val_labels, val_transform)

    train_loader = DataLoader(train_dataset, batch_size=config["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config["batch_size"], shuffle=False)

    return train_loader, val_loader, class_names


# ----------------------
# 模型定义（保留ResNet50但可切换轻量模型）
# ----------------------
def create_model(use_pretrained=True):
    model = models.resnet50(pretrained=use_pretrained)
    num_ftrs = model.fc.in_features
    # 添加 Dropout 层
    dropout_rate = 0.5  # Dropout 概率，通常设置为 0.5
    model.fc = nn.Sequential(
        nn.Dropout(dropout_rate),
        nn.Linear(num_ftrs, config["num_classes"])
    )

    # 可选：替换为轻量模型（如MobileNetV3）
    # model = models.mobilenet_v3_small(pretrained=True)
    # model.classifier[3] = nn.Linear(1024, config["num_classes"])

    return model


# ----------------------
# 训练与验证函数
# ----------------------
def train_model(model, criterion, optimizer, train_loader, val_loader):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    best_acc = 0.0
    for epoch in range(config["num_epochs"]):
        # 训练阶段
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)

        # 验证阶段
        val_acc = evaluate(model, val_loader, device)

        print(f"Epoch {epoch + 1}/{config['num_epochs']}")
        print(f"Train Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f}")

        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), "best_model.pth")

    print(f"Training complete. Best Val Acc: {best_acc:.4f}")


def evaluate(model, val_loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total


# ----------------------
# 预测函数
# ----------------------
def predict(image_path, model, class_names):
    model.load_state_dict(torch.load("best_model.pth"))
    model.eval()
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    try:
        image = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Image file {image_path} not found.")
        return None
    image = transform(image).unsqueeze(0)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    image = image.to(device)
    with torch.no_grad():
        output = model(image)
        _, pred = torch.max(output, 1)
    return class_names[pred.item()]


# ----------------------
# 批量重命名函数
# ----------------------
def batch_rename_images(test_folder, model, class_names):
    for filename in os.listdir(test_folder):
        if filename.endswith(('.jpg')):
            image_path = os.path.join(test_folder, filename)
            predicted_class = predict(image_path, model, class_names)
            if predicted_class:
                # 提取文件名中的数字部分
                number_part = ''.join(filter(str.isdigit, filename))
                new_filename = f"{predicted_class}-{number_part}.jpg"
                new_path = os.path.join(test_folder, new_filename)
                os.rename(image_path, new_path)
                print(f"Renamed {filename} to {new_filename}")


# ----------------------
# 主程序
# ----------------------
if __name__ == "__main__":
    # 检查CUDA可用性
    print(f"CUDA available: {torch.cuda.is_available()}")

    # 准备数据
    train_loader, val_loader, class_names = prepare_dataloaders()
    print(f"Class names: {class_names}")

    # 初始化模型
    model = create_model(use_pretrained=True)
    criterion = nn.CrossEntropyLoss()
    # 添加 L2 正则化，weight_decay 通常设置为一个较小的值，如 0.0001
    optimizer = optim.Adam(model.parameters(), lr=config["lr"], weight_decay=0.0001)

    # 训练模型
    train_model(model, criterion, optimizer, train_loader, val_loader)

    # 批量重命名测试文件夹中的图片
    test_folder = "./test"
    batch_rename_images(test_folder, model, class_names)