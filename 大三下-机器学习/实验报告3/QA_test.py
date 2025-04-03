import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import json
from tqdm import tqdm

# 加载数据、模型、分词器
device = "cuda" if torch.cuda.is_available() else "cpu"
data_path = './ChineseSquad/test.json'
model_path = './bert_qa_model_128_4'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForQuestionAnswering.from_pretrained(model_path).to(device)

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

total_questions = 0
correct_answers = 0
max_question_len = 60
max_paragraph_len = 150
doc_stride = 150
max_seq_len = 1 + max_question_len + 1 + max_paragraph_len + 1

# 设置种子
def same_seeds(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

same_seeds(42)


def padding(ids_q, ids_p):
    pad_len = max_seq_len - len(ids_q) - len(ids_p)
    input_ids = ids_q + ids_p + [0] * pad_len
    token_type_ids = [0] * len(ids_q) + [1] * len(ids_p) + [0] * pad_len
    attention_mask = [1] * (len(ids_q) + len(ids_p)) + [0] * pad_len
    return input_ids, token_type_ids, attention_mask


def evaluate(context, input_ids_list, offset_mapping_list, outputs):
    max_prob = -float('inf')
    best_ans = ''
    for k in range(len(input_ids_list)):
        start_logits = outputs.start_logits[k]
        end_logits = outputs.end_logits[k]
        start_prob, start_idx = torch.max(start_logits, dim=0)
        end_prob, end_idx = torch.max(end_logits, dim=0)
        start_idx = start_idx.item()
        end_idx = end_idx.item()
        # 添加边界检查
        offset_mapping = offset_mapping_list[k]
        if start_idx < len(offset_mapping) and end_idx < len(offset_mapping) and start_idx <= end_idx:
            if start_prob + end_prob > max_prob:
                max_prob = start_prob + end_prob
                # 通过offset_mapping定位原始文本
                start_char = offset_mapping[start_idx][0]
                end_char = offset_mapping[end_idx][1]
                best_ans = context[start_char:end_char].strip()
    return best_ans


def answer_question(context, question):
    # 分词并获取offset_mapping
    tokenized_question = tokenizer(question, add_special_tokens=False)
    tokenized_paragraph = tokenizer(context, add_special_tokens=False, return_offsets_mapping=True)

    input_ids_list = []
    token_type_ids_list = []
    attention_mask_list = []
    offset_mapping_list = []  # 新增：保存每个分块的offset_mapping

    for i in range(0, len(tokenized_paragraph["input_ids"]), doc_stride):
        # 处理问题部分
        input_ids_q = [101] + tokenized_question["input_ids"][:max_question_len] + [102]
        # 处理段落分块
        chunk_ids = tokenized_paragraph["input_ids"][i:i + max_paragraph_len]
        chunk_offset = tokenized_paragraph["offset_mapping"][i:i + max_paragraph_len]
        input_ids_p = chunk_ids + [102]
        input_ids, token_type_ids, attention_mask = padding(input_ids_q, input_ids_p)

        input_ids_list.append(input_ids)
        token_type_ids_list.append(token_type_ids)
        attention_mask_list.append(attention_mask)
        # 将offset_mapping对齐到分块后的input_ids_p
        offset_mapping = [(0, 0)] * len(input_ids_q) + chunk_offset + [(0, 0)]  # [CLS]Q[SEP]P[SEP]
        offset_mapping_list.append(offset_mapping)

    input_ids = torch.tensor(input_ids_list).to(device)
    token_type_ids = torch.tensor(token_type_ids_list).to(device)
    attention_mask = torch.tensor(attention_mask_list).to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            attention_mask=attention_mask
        )

    return evaluate(context, input_ids_list, offset_mapping_list, outputs)


# 统计问题总数
total_questions = sum(len(paragraph['qas']) for item in data['data'] for paragraph in item['paragraphs'])

# 遍历数据，以问题总数为总任务设置进度条
with tqdm(total=total_questions, desc="Processing questions") as pbar:
    for item in data['data']:
        for paragraph in item['paragraphs']:
            context = paragraph['context']
            for qa in paragraph['qas']:
                question = qa['question']
                # 假设我们已经知道标准答案
                standard_answers = [ans['text'] for ans in qa['answers']]
                # 这里模拟你输入的答案
                # 我们直接用标准答案作为输入答案来测试
                input_answer = answer_question(context, question)
                if input_answer in standard_answers:
                    correct_answers += 1
                pbar.update(1)

# 计算正确率
accuracy = correct_answers / total_questions if total_questions > 0 else 0

print(f"使用模型: {model_path}")
print(f"总问题个数: {total_questions}")
print(f"回答正确问题个数: {correct_answers}")
print(f"正确率: {accuracy:.2%}")