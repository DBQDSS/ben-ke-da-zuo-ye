import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup

# ================== 配置中文字体 ==================
plt.rcParams["font.family"] = ["SimHei"]  # 使用中文字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ================== 配置参数 ==================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
batch_size = 4               # 推荐值：16 或 32
lr = 3e-5                     # 推荐值：2e-5 或 3e-5
epochs = 10                   # 推荐值：3-5，但可以尝试10轮
patience = 3                  # 早停：验证集连续2轮无提升则停止
model_save_path = 'model4.pth'
bert_path = './bert-base-chinese'

# ================== 数据加载 ==================
class NewsDataset(Dataset):
    def __init__(self, file_path, tokenizer, label_encoder=None):
        df = pd.read_csv(file_path, sep='\t')
        self.encodings = tokenizer(df['text_a'].tolist(), truncation=True, padding=True, max_length=512)
        if label_encoder is None:
            self.label_encoder = LabelEncoder()
            self.labels = self.label_encoder.fit_transform(df['label'])
        else:
            self.label_encoder = label_encoder
            self.labels = self.label_encoder.transform(df['label'])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        # 将标签的数据类型转换为 Long
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

# 加载预训练的tokenizer
tokenizer = BertTokenizer.from_pretrained(bert_path)

# 初始化数据集
train_dataset = NewsDataset('thu_news/train.txt', tokenizer)
valid_dataset = NewsDataset('thu_news/valid.txt', tokenizer, train_dataset.label_encoder)
test_dataset = NewsDataset('thu_news/test.txt', tokenizer, train_dataset.label_encoder)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

num_classes = len(train_dataset.label_encoder.classes_)

# ================== 模型定义 ==================
model = BertForSequenceClassification.from_pretrained(bert_path, num_labels=num_classes, ignore_mismatched_sizes=True).to(device)

# 优化器和调度器
optimizer = optim.AdamW(model.parameters(), lr=lr)
total_steps = len(train_loader) * epochs
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

# 损失函数
criterion = nn.CrossEntropyLoss()

# ================== 早停初始化 ==================
best_accuracy = 0
no_improve_epochs = 0

# ================== 训练模型 ==================
train_losses, valid_losses, valid_accuracies = [], [], []

for epoch in range(epochs):
    model.train()
    total_loss = 0
    progress_bar = tqdm(train_loader, desc=f"第 {epoch + 1} 轮训练")

    for batch in progress_bar:
        batch = {k: v.to(device) for k, v in batch.items()}
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss
        logits = outputs.logits
        loss.backward()
        optimizer.step()
        scheduler.step()
        total_loss += loss.item()
        progress_bar.set_postfix({'loss': loss.item()})

    avg_train_loss = total_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # 验证
    model.eval()
    valid_loss = 0
    all_preds, all_labels = [], []
    with torch.no_grad():
        for batch in valid_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            logits = outputs.logits
            valid_loss += loss.item()
            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(batch['labels'].cpu().numpy())

    avg_valid_loss = valid_loss / len(valid_loader)
    valid_losses.append(avg_valid_loss)
    accuracy = accuracy_score(all_labels, all_preds)
    valid_accuracies.append(accuracy)
    print(f"验证集 Loss: {avg_valid_loss:.4f}, 准确率: {accuracy:.4f}")

    # ================== 早停判断 ==================
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        no_improve_epochs = 0
        torch.save(model.state_dict(), model_save_path)
        print(f"验证集准确率提升，模型已保存：{best_accuracy:.4f}")
    else:
        no_improve_epochs += 1
        print(f"验证集准确率无提升（连续 {no_improve_epochs} 次）")
        if no_improve_epochs >= patience:
            print(f"早停：连续 {patience} 轮无提升，提前结束训练")
            break

# ================== 绘制图像 ==================
actual_epochs = len(train_losses)
plt.figure()
plt.plot(range(1, actual_epochs + 1), train_losses, label='训练损失')
plt.plot(range(1, actual_epochs + 1), valid_losses, label='验证损失')
plt.xlabel('轮数')
plt.ylabel('损失')
plt.title('训练与验证损失')
plt.legend()
plt.savefig('Loss4.jpg')

plt.figure()
plt.plot(range(1, actual_epochs + 1), valid_accuracies, label='验证准确率')
plt.xlabel('轮数')
plt.ylabel('准确率')
plt.title('验证集准确率')
plt.legend()
plt.savefig('Accuracy4.jpg')

# ================== 测试模型 ==================
model.load_state_dict(torch.load(model_save_path))
model.eval()
all_preds, all_labels = [], []
with torch.no_grad():
    for batch in test_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(batch['labels'].cpu().numpy())
test_accuracy = accuracy_score(all_labels, all_preds)
print(f"测试集准确率: {test_accuracy:.4f}")