import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

def same_seeds(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


device = "cuda" if torch.cuda.is_available() else "cpu"
same_seeds(42)

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained("./bert_qa_model_128_4")
model = AutoModelForQuestionAnswering.from_pretrained("./bert_qa_model_128_4").to(device)
model.eval()

max_question_len = 60
max_paragraph_len = 150
doc_stride = 150
max_seq_len = 1 + max_question_len + 1 + max_paragraph_len + 1


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
        if start_prob + end_prob > max_prob and start_idx <= end_idx:
            max_prob = start_prob + end_prob
            # 通过offset_mapping定位原始文本
            offset_mapping = offset_mapping_list[k]
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


if __name__ == "__main__":
    context = ("数学与应用数学（强基计划）专业依托数学与统计学院，学院拥有悠久的办学历史、良好的学科声誉，以及业界共识的应用数学与交叉学科领先地位。其前身是创建于1928年的交通大学数学系，其数学学科连续两次教育部学科评估均在前5%（A档），ESI科排名位列全球学前1%。强基计划数学类的课程设置非常丰富————机器学习就是西安交通大学数学强基专业大三下学期的一门专业课，任课教师是数学学院的孟德宇老师。")
    question = "谁教机器学习？"

    answer = answer_question(context, question)
    print(f"问题：{question}")
    print(f"答案：{answer}")

    # context = "数学与应用数学（强基计划）专业依托数学与统计学院，学院拥有悠久的办学历史、良好的学科声誉，以及业界共识的应用数学与交叉学科领先地位。其前身是创建于1928年的交通大学数学系，其数学学科连续两次教育部学科评估均在前5%（A档），ESI科排名位列全球学前1%。强基计划数学类的课程设置非常丰富————机器学习就是西安交通大学数学强基专业大三下学期的一门专业课，任课教师是数学学院的孟德宇老师。"
    # question = "谁教机器学习？"

    # context = "美国广播公司（ABC）是一家美国商业广播电视网络公司，隶属于迪斯尼-ABC电视集团，是迪斯尼公司迪斯尼媒体网络分部的子公司。这个电视网是三大电视网的一部分。该网络的总部设在哥伦布大道和曼哈顿西66街，在纽约市、洛杉矶和加州伯班克设有其他主要办事处和生产设施。"
    # question = "什么公司拥有美国广播公司？"