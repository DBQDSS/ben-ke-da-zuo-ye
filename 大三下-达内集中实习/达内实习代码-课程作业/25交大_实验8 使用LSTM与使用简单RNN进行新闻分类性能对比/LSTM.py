# 导入包
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from torch.nn.utils.rnn import pad_sequence
from torchtext.vocab import build_vocab_from_iterator

# 配置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ================== 配置参数 ==================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
batch_size = 64
lr = 0.001
epochs = 50
embedding_dim = 128
hidden_dim = 128
model_save_path = 'model2.pth'  # 修改保存路径
patience = 10
# ================== 数据加载 ==================
class NewsDataset(Dataset):
    def __init__(self, file_path, vocab=None, label_encoder=None):
        df = pd.read_csv(file_path, sep='\t')
        self.texts = df['text_a'].astype(str).tolist()
        self.labels = df['label'].tolist()

        # 编码标签
        if label_encoder is None:
            self.label_encoder = LabelEncoder()
            self.labels = self.label_encoder.fit_transform(self.labels)
        else:
            self.label_encoder = label_encoder
            self.labels = self.label_encoder.transform(self.labels)

        # 构建词汇表
        if vocab is None:
            self.vocab = build_vocab_from_iterator(self.tokenize(self.texts), specials=["<pad>", "<unk>"])
            self.vocab.set_default_index(self.vocab["<unk>"])
        else:
            self.vocab = vocab

        self.texts = [torch.tensor(self.vocab(token), dtype=torch.long) for token in self.tokenize(self.texts)]

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

    def tokenize(self, texts):
        return [list(text) for text in texts]  # 按字符分词


def collate_fn(batch):
    texts, labels = zip(*batch)
    lengths = torch.tensor([len(seq) for seq in texts], dtype=torch.long)
    padded_texts = pad_sequence(texts, batch_first=True, padding_value=0)
    labels = torch.tensor(labels, dtype=torch.long)
    return padded_texts, lengths, labels


train_dataset = NewsDataset('thu_news/train.txt')
valid_dataset = NewsDataset('thu_news/valid.txt', vocab=train_dataset.vocab, label_encoder=train_dataset.label_encoder)
test_dataset = NewsDataset('thu_news/test.txt', vocab=train_dataset.vocab, label_encoder=train_dataset.label_encoder)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

num_classes = len(train_dataset.label_encoder.classes_)

# ================== 模型定义（使用LSTM） ==================
class SimpleLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SimpleLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, lengths):
        embedded = self.embedding(x)
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, lengths.cpu(), batch_first=True,
                                                            enforce_sorted=False)
        packed_output, (hidden, cell) = self.lstm(packed_embedded)
        return self.fc(hidden[-1])  # 取最后一个隐藏状态

model = SimpleLSTM(len(train_dataset.vocab), embedding_dim, hidden_dim, num_classes).to(device)

# ================== 损失函数和优化器 ==================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

# ================== 早停初始化 ==================
best_accuracy = 0
no_improve_epochs = 0

# ================== 训练模型 ==================
train_losses, valid_losses, valid_accuracies = [], [], []

for epoch in range(epochs):
    model.train()
    total_loss = 0
    progress_bar = tqdm(train_loader, desc=f"第 {epoch + 1} 轮训练")

    for texts, lengths, labels in progress_bar:
        texts, lengths, labels = texts.to(device), lengths.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(texts, lengths)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        progress_bar.set_postfix({'loss': loss.item()})

    avg_train_loss = total_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # 验证
    model.eval()
    valid_loss = 0
    all_preds, all_labels = [], []
    with torch.no_grad():
        for texts, lengths, labels in valid_loader:
            texts, lengths, labels = texts.to(device), lengths.to(device), labels.to(device)
            outputs = model(texts, lengths)
            loss = criterion(outputs, labels)
            valid_loss += loss.item()
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
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
        print(f"模型提升：保存新模型（准确率: {best_accuracy:.4f}）")
    else:
        no_improve_epochs += 1
        print(f"连续 {no_improve_epochs} 轮无提升")
        if no_improve_epochs >= patience:
            print(f"早停：连续 {patience} 轮无提升，提前结束训练")
            break

# ================== 绘制图像（修改命名） ==================
plt.figure()
plt.plot(range(1, len(train_losses) + 1), train_losses, label='训练损失')
plt.plot(range(1, len(valid_losses) + 1), valid_losses, label='验证损失')
plt.xlabel('轮数')
plt.ylabel('损失')
plt.title('训练与验证损失')
plt.legend()
plt.savefig('Loss2.jpg')

plt.figure()
plt.plot(range(1, len(valid_accuracies) + 1), valid_accuracies, label='验证准确率')
plt.xlabel('轮数')
plt.ylabel('准确率')
plt.title('验证集准确率')
plt.legend()
plt.savefig('Accuracy2.jpg')

# ================== 测试模型 ==================
model.load_state_dict(torch.load(model_save_path))
model.eval()
all_preds, all_labels = [], []
with torch.no_grad():
    for texts, lengths, labels in test_loader:
        texts, lengths, labels = texts.to(device), lengths.to(device), labels.to(device)
        outputs = model(texts, lengths)
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
test_accuracy = accuracy_score(all_labels, all_preds)
print(f"测试集准确率: {test_accuracy:.4f}")
