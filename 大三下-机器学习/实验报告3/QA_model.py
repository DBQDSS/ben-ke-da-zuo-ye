import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast, BertForQuestionAnswering
from torch.optim import AdamW
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# 设置绘图风格，使用seaborn的美观配色
sns.set_style("whitegrid")
sns.set_palette("husl")

# 配置参数
MAX_LEN = 512
BATCH_SIZE = 4  # 减小batch_size防止显存不足
EPOCHS = 1
LEARNING_RATE = 3e-5
TRAIN_PATH = "./ChineseSquad/train.json"
DEV_PATH = "./ChineseSquad/dev.json"
MODEL_PATH = "./bert_qa_model_512_3e-5_4_128"

# 新增滑动窗口参数
STRIDE = 128  # 滑动窗口的步长

# 数据预处理（增加容错处理）
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['data']


def preprocess_data(data):
    processed = []
    for article in data:
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            for qa in paragraph['qas']:
                # 增强空答案处理
                if not qa.get('answers') or len(qa['answers']) == 0:
                    continue
                answer = qa['answers'][0]
                # 验证answer_start有效性
                if answer['answer_start'] >= len(context):
                    continue
                processed.append({
                    'context': context,
                    'question': qa['question'],
                    'answer_text': answer['text'],
                    'start_pos': answer['answer_start'],
                    'end_pos': answer['answer_start'] + len(answer['text'])
                })
    return processed


# 数据集类（使用Fast Tokenizer）
class SquadDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        encodings = self.tokenizer.encode_plus(
            item['question'],
            item['context'],
            add_special_tokens=True,
            max_length=MAX_LEN,
            padding='max_length',
            truncation=True,
            return_offsets_mapping=True,
            stride=STRIDE,
            return_overflowing_tokens=True
        )

        input_ids = encodings['input_ids']
        attention_mask = encodings['attention_mask']
        offset_mapping = encodings['offset_mapping']
        overflow_to_sample_mapping = encodings['overflow_to_sample_mapping']

        start_pos = item['start_pos']
        end_pos = item['end_pos']

        all_start_positions = []
        all_end_positions = []

        for i in range(len(input_ids)):
            sample_idx = overflow_to_sample_mapping[i]
            offset = offset_mapping[i]
            start_idx = end_idx = 0

            for token_idx, (char_start, char_end) in enumerate(offset):
                if char_start <= start_pos < char_end:
                    start_idx = token_idx
                if char_start < end_pos <= char_end:
                    end_idx = token_idx
                if char_end > end_pos:
                    break

            all_start_positions.append(start_idx)
            all_end_positions.append(end_idx)

        result = []
        for i in range(len(input_ids)):
            result.append({
                'input_ids': torch.tensor(input_ids[i], dtype=torch.long),
                'attention_mask': torch.tensor(attention_mask[i], dtype=torch.long),
                'start_positions': torch.tensor(all_start_positions[i], dtype=torch.long),
                'end_positions': torch.tensor(all_end_positions[i], dtype=torch.long)
            })

        return result


# 训练函数
def train():
    # 初始化模型和FastTokenizer
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
    model = BertForQuestionAnswering.from_pretrained('bert-base-chinese')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # 加载数据
    train_data = preprocess_data(load_data(TRAIN_PATH))
    dev_data = preprocess_data(load_data(DEV_PATH))

    train_dataset = SquadDataset(train_data, tokenizer)
    dev_dataset = SquadDataset(dev_data, tokenizer)

    # 展开数据集
    train_flat_dataset = []
    for item in train_dataset:
        train_flat_dataset.extend(item)
    dev_flat_dataset = []
    for item in dev_dataset:
        dev_flat_dataset.extend(item)

    train_loader = DataLoader(train_flat_dataset, batch_size=BATCH_SIZE, shuffle=True)
    dev_loader = DataLoader(dev_flat_dataset, batch_size=BATCH_SIZE)

    # 使用PyTorch的AdamW优化器
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

    train_losses = []
    val_losses = []
    step_count = 0

    # 训练循环
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0

        # 使用tqdm显示训练进度
        train_progress = tqdm(train_loader, desc=f'Epoch {epoch + 1}/{EPOCHS} Training')
        for batch in train_progress:
            optimizer.zero_grad()

            inputs = {
                'input_ids': batch['input_ids'].to(device),
                'attention_mask': batch['attention_mask'].to(device),
                'start_positions': batch['start_positions'].to(device),
                'end_positions': batch['end_positions'].to(device)
            }

            outputs = model(**inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            train_losses.append(loss.item())
            step_count += 1
            train_progress.set_postfix({'Train Loss': total_loss / (train_progress.n + 1)})

        # 验证损失
        model.eval()
        val_loss = 0
        # 使用tqdm显示验证进度
        dev_progress = tqdm(dev_loader, desc=f'Epoch {epoch + 1}/{EPOCHS} Validation')
        with torch.no_grad():
            for batch in dev_progress:
                inputs = {
                    'input_ids': batch['input_ids'].to(device),
                    'attention_mask': batch['attention_mask'].to(device),
                    'start_positions': batch['start_positions'].to(device),
                    'end_positions': batch['end_positions'].to(device)
                }
                outputs = model(**inputs)
                val_loss += outputs.loss.item()
                val_losses.append(outputs.loss.item())
                dev_progress.set_postfix({'Val Loss': val_loss / (dev_progress.n + 1)})

    # 绘制训练损失和验证损失曲线，设置颜色
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(train_losses)), train_losses, label='Training Loss', marker='o', color='#70FFE2')
    plt.plot(range(len(val_losses)), val_losses, label='Validation Loss', marker='s', color='#FF6C6C')
    plt.title('Training and Validation Loss by Step')
    plt.xlabel('Training Step')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{MODEL_PATH}.png")
    plt.show()

    # 保存模型
    model.save_pretrained(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)
    return model, tokenizer


# 预测函数（保持不变）
def answer_question(context, question, model, tokenizer):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    inputs = tokenizer.encode_plus(
        question,
        context,
        add_special_tokens=True,
        max_length=MAX_LEN,
        padding='max_length',
        truncation=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    start_idx = torch.argmax(outputs.start_logits)
    end_idx = torch.argmax(outputs.end_logits) + 1

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    answer_tokens = tokens[start_idx:end_idx]
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

    answer = answer.replace('[CLS]', '').replace('[SEP]', '').strip()
    return answer


if __name__ == "__main__":
    # 训练模型
    model, tokenizer = train()
    print("训练完毕。")