# 环境配置
import torch
import numpy as np
import matplotlib.pyplot as plt

# 设置设备（自动检测CUDA）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# =====================================================
# 1. 数据准备
# 1.1 读取数据
data_X = []
data_Y = []
# 性别映射（M：雄性，F：雌性，I：未成年）
sex_map = {'I': 0, 'M': 1, 'F': -1}
with open('AbaloneAgePrediction.txt') as f:
    for line in f.readlines():
        line = line.split(',')
        line[0] = sex_map[line[0]]  # 转换性别为数值
        data_X.append(line[:-1])  # 前8列为特征
        data_Y.append(line[-1:])  # 最后一列为环数（年龄）

# 转换为numpy数组
data_X = np.array(data_X, dtype='float32')
data_Y = np.array(data_Y, dtype='float32')
print('数据形状:', data_X.shape, data_Y.shape)
print('特征维度:', data_X.shape[1])

# 1.2数据归一化
for i in range(data_X.shape[1]):
    _min = np.min(data_X[:, i])
    _max = np.max(data_X[:, i])
    data_X[:, i] = (data_X[:, i] - _min) / (_max - _min)  # 归一化到[0,1]

# 1.3划分数据集
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    data_X, data_Y, test_size=0.2, random_state=1
)

# 拼接特征和标签
train_data = np.concatenate((X_train, y_train), axis=1)
test_data = np.concatenate((X_test, y_test), axis=1)
print('训练集形状:', train_data.shape)
print('测试集形状:', test_data.shape)

# =====================================================
# 2. 网络配置
class Regressor(torch.nn.Module):
    def __init__(self):
        super(Regressor, self).__init__()
        # 定义线性层：8个特征输入，1个输出
        self.fc = torch.nn.Linear(8, 1)

    def forward(self, inputs):
        return self.fc(inputs)

# =====================================================
# 3. 网络训练与评估

train_nums = []
train_costs = []

# 3.1 绘制训练损失曲线（添加保存功能）
def draw_train_process(epochs, costs):
    plt.figure()
    plt.plot(epochs, costs, color='red', label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Curve')
    plt.legend()
    plt.grid(True)
    plt.savefig('loss1.jpg')  # 保存损失图像
    plt.show()

# 3.2 训练函数
import torch.nn.functional as F

BATCH_SIZE = 50

def train(model):
    print('开始训练...')
    model.train()  # 训练模式
    EPOCH_NUM = 100
    optimizer = torch.optim.SGD(model.parameters(), lr=0.0001)
    epochs = []
    epoch_costs = []

    for epoch_id in range(EPOCH_NUM):
        np.random.shuffle(train_data)
        mini_batches = [train_data[k:k + BATCH_SIZE] for k in range(0, len(train_data), BATCH_SIZE)]
        batch_costs = []

        for batch_id, data in enumerate(mini_batches):
            # 转换为PyTorch张量并移至设备
            features = torch.tensor(data[:, :8], dtype=torch.float32).to(device)
            labels = torch.tensor(data[:, -1:], dtype=torch.float32).to(device)

            # 前向传播
            y_pred = model(features)
            cost = F.mse_loss(y_pred, labels)
            batch_costs.append(cost.item())

            # 反向传播
            optimizer.zero_grad()  # 清空梯度
            cost.backward()  # 计算梯度
            optimizer.step()  # 更新参数

        # 计算epoch平均损失
        epoch_loss = np.mean(batch_costs)
        epochs.append(epoch_id)
        epoch_costs.append(epoch_loss)

        if epoch_id % 10 == 0:
            print(f"Epoch: {epoch_id}, Average Loss: {epoch_loss:.5f}")

    return epochs, epoch_costs


# 3.3 初始化模型并训练
model = Regressor().to(device)  # 将模型移至设备
epochs, epoch_costs = train(model)
draw_train_process(epochs, epoch_costs)

# 保存模型（训练完成后保存）
torch.save(model.state_dict(), 'model1.pth')
print("模型已保存为 model1.pth")

# =====================================================
# 4. 模型预测
# 4.1 可视化真实值与预测值（添加保存功能）
def draw_infer_result(groud_truths, infer_results):
    plt.title('Abalone Age Prediction', fontsize=24)
    x = np.arange(1, 20)
    plt.plot(x, x, label='Ideal Prediction')  # 理想预测线
    plt.xlabel('Ground Truth', fontsize=14)
    plt.ylabel('Infer Result', fontsize=14)
    plt.scatter(groud_truths, infer_results, color='green', label='Predictions')
    plt.legend()
    plt.grid()
    plt.savefig('predict1.jpg')  # 保存预测可视化图像
    plt.show()


# 预测测试集数据
INFER_BATCH_SIZE = 15
infer_features = torch.tensor(test_data[:, :8], dtype=torch.float32).to(device)  # 移至设备
infer_labels = test_data[:, -1]

# 模型评估模式
model.eval()
with torch.no_grad():  # 关闭梯度计算
    fetch_list = model(infer_features)

# 展示部分预测结果
infer_results = []
groud_truths = []
sum_cost = 0
for i in range(INFER_BATCH_SIZE):
    infer_result = fetch_list[i].item()  # 自动移回CPU
    ground_truth = infer_labels[i]
    infer_results.append(infer_result)
    groud_truths.append(ground_truth)
    print(f"No.{i}: 预测值 {infer_result:.2f}, 真实值 {ground_truth:.2f}")
    sum_cost += (infer_result - ground_truth) ** 2

mean_loss = sum_cost / INFER_BATCH_SIZE
print(f"平均损失: {mean_loss:.4f}")
draw_infer_result(groud_truths, infer_results)


# 4.2 按行预测数据集
def predict_dataset(row):
    if row < 0 or row >= len(data_X):
        print("输入行数超出范围！")
        return
    sample = torch.tensor(data_X[row].reshape(1, -1), dtype=torch.float32).to(device)  # 移至设备
    model.eval()
    with torch.no_grad():
        prediction = model(sample)
    print(f"第 {row} 行数据的预测年龄: {prediction.item():.2f}")  # 自动移回CPU
# 示例调用：predict_dataset(15)


# 4.3 用户输入预测
def predict_user_input():
    try:
        input_str = input("请输入8个特征（用逗号分隔）: ")
        input_list = [float(x) for x in input_str.split(',')]
        if len(input_list) != 8:
            print("必须输入8个特征！")
            return

        # 归一化用户输入
        input_array = np.array(input_list, dtype=np.float32)
        for i in range(8):
            _min = np.min(data_X[:, i])
            _max = np.max(data_X[:, i])
            input_array[i] = (input_array[i] - _min) / (_max - _min)

        # 转换为张量并预测
        sample = torch.tensor(input_array.reshape(1, -1), dtype=torch.float32).to(device)  # 移至设备
        model.eval()
        with torch.no_grad():
            prediction = model(sample)
        print(f"预测年龄: {prediction.item():.2f}")  # 自动移回CPU
    except ValueError:
        print("输入格式错误，请输入数字！")


if __name__ == '__main__':
    while True:
        print("请输入：")
        print("1表示要对数据集中某行预测，2表示要对输入数据做预测，q表示退出")
        a = input()
        if a == '1':
            print("请输入一个行数")
            row = int(input())
            predict_dataset(row)
        elif a == '2':
            predict_user_input()
        elif a == 'q':
            break
        else:
            print("请输入符合规则的数字")