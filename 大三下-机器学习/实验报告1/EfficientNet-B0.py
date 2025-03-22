# anime_classifier_local.py
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models, utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
from tqdm import tqdm

# ----------------------
# 本地配置参数
# ----------------------
config = {
    "data_dir": "./archive/Data",
    "batch_size": 32,
    "image_size": 224,
    "num_epochs": 15,
    "lr": 0.001,
    "num_classes": 5
}

# ----------------------
# 可视化设置
# ----------------------
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", font_scale=1.2)
try:
    plt.rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
except:
    pass
COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD"]


# ----------------------
# 数据集类
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
    all_image_paths = []
    labels = []
    class_names = sorted(os.listdir(config["data_dir"]))

    for label, class_name in enumerate(class_names):
        class_dir = os.path.join(config["data_dir"], class_name)
        for img_file in os.listdir(class_dir):
            if img_file.endswith(('.jpg', '.png')):
                all_image_paths.append(os.path.join(class_dir, img_file))
                labels.append(label)

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        all_image_paths, labels, test_size=0.2, random_state=42
    )

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
# 模型定义
# ----------------------
def create_model(use_pretrained=True):
    model = models.efficientnet_b0(pretrained=use_pretrained)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, config["num_classes"])
    return model


# ----------------------
# 可视化函数
# ----------------------
def plot_data_samples(dataloader, class_names, n=8):
    images, labels = next(iter(dataloader))
    images = images[:n]
    labels = labels[:n]

    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    images = images.numpy().transpose((0, 2, 3, 1))
    images = std * images + mean
    images = np.clip(images, 0, 1)

    plt.figure(figsize=(12, 6))
    for i in range(n):
        ax = plt.subplot(2, 4, i + 1)
        ax.imshow(images[i])
        ax.set_title(class_names[labels[i]], color='black')
        ax.axis('off')
    plt.suptitle("Augmented Training Samples", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig("data_samples.png", bbox_inches='tight')
    plt.show()


def plot_training_curves(train_losses, val_accuracies):
    plt.figure(figsize=(8, 5))

    # 绘制训练损失曲线
    ax1 = plt.gca()
    line1 = ax1.plot(train_losses, color=COLORS[0], lw=2, marker='o', markersize=8, label='Training Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    # 设置左侧Y轴为5段 (6个刻度)
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))  # 关键修改
    ax1.set_ylim(0, 1)  # 保持原有范围限制

    # 创建第二个Y轴用于准确率
    ax2 = ax1.twinx()
    line2 = ax2.plot(val_accuracies, color=COLORS[1], lw=2, marker='s', markersize=8, label='Validation Accuracy')
    ax2.set_ylabel('Accuracy (%)', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # 设置右侧Y轴为5段 (6个刻度)
    ax2.yaxis.set_major_locator(MultipleLocator(4))  # 关键修改
    ax2.set_ylim(80, 100)  # 保持原有范围限制

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title("Training Loss and Validation Accuracy Curves")
    plt.tight_layout()
    plt.savefig("training_curves.png", bbox_inches='tight')
    plt.show()



def plot_confusion_matrix(model, dataloader, class_names, device):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in tqdm(dataloader, desc="Generating Confusion Matrix"):
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    cm = confusion_matrix(all_labels, all_preds)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.savefig("confusion_matrix.png", bbox_inches='tight')
    plt.show()


def visualize_predictions(test_folder, model, class_names, device, n=8):
    model.load_state_dict(torch.load("best_model.pth"))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    plt.figure(figsize=(12, 8))
    count = 0
    for filename in os.listdir(test_folder):
        if count >= n:
            break
        if filename.endswith(('.jpg')):
            image_path = os.path.join(test_folder, filename)
            try:
                image = Image.open(image_path).convert('RGB')
                input_tensor = transform(image).unsqueeze(0).to(device)

                with torch.no_grad():
                    output = model(input_tensor)
                    probs = torch.nn.functional.softmax(output, dim=1)
                    conf, pred = torch.max(probs, 1) # 输出最大相似度的

                image_np = input_tensor.cpu().squeeze().numpy().transpose((1, 2, 0))
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                image_np = std * image_np + mean
                image_np = np.clip(image_np, 0, 1)

                ax = plt.subplot(2, 4, count + 1)
                ax.imshow(image_np)
                title = f"Pred: {class_names[pred.item()]}\nConf: {conf.item():.8f}" # 相似度
                ax.set_title(title, color='black')
                ax.axis('off')
                count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    plt.suptitle("Prediction Examples", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig("prediction_examples.png", bbox_inches='tight')
    plt.show()


# ----------------------
# 训练验证函数
# ----------------------
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


def train_model(model, criterion, optimizer, train_loader, val_loader):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    train_losses = []
    val_accuracies = []
    best_acc = 0.0

    plot_data_samples(train_loader, class_names)

    for epoch in range(config["num_epochs"]):
        model.train()
        running_loss = 0.0
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{config['num_epochs']}")

        for inputs, labels in progress_bar:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            progress_bar.set_postfix(loss=loss.item())

        epoch_loss = running_loss / len(train_loader.dataset)
        train_losses.append(epoch_loss)

        val_acc = evaluate(model, val_loader, device)
        val_accuracies.append(val_acc * 100)

        print(f"\nEpoch {epoch + 1}/{config['num_epochs']}")
        print(f"Train Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.2%}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), "best_model.pth")

    plot_training_curves(train_losses, val_accuracies)
    plot_confusion_matrix(model, val_loader, class_names, device)
    print(f"\nTraining complete. Best Val Acc: {best_acc:.2%}")

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
                number_part = ''.join(filter(str.isdigit, filename))
                new_filename = f"{predicted_class}-{number_part}.jpg"
                new_path = os.path.join(test_folder, new_filename)
                os.rename(image_path, new_path)
                print(f"Renamed {filename} to {new_filename}")


# ----------------------
# 主程序
# ----------------------
if __name__ == "__main__":
    print(f"CUDA available: {torch.cuda.is_available()}")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    train_loader, val_loader, class_names = prepare_dataloaders()
    print(f"Class names: {class_names}")

    model = create_model(use_pretrained=True).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config["lr"], weight_decay=0.0001)

    train_model(model, criterion, optimizer, train_loader, val_loader)

    test_folder = "./test"
    visualize_predictions(test_folder, model, class_names, device)
    batch_rename_images(test_folder, model, class_names)