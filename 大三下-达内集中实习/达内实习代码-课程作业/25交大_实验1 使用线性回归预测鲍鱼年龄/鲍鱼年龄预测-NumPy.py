import numpy as np
import matplotlib.pyplot as plt

# =====================
# 1. 数据准备
# =====================

# 1.1 读取数据
data_X = []
data_Y = []

# 性别映射（M：雄性，F：雌性，I：未成年）
sex_map = {'I': 0, 'M': 1, 'F': -1}
with open('AbaloneAgePrediction.txt') as f:
    for line in f.readlines():
        line = line.strip().split(',')
        line[0] = sex_map[line[0]]  # 将性别字符转换为数值
        data_X.append(line[:-1])    # 前8列为特征
        data_Y.append(line[-1:])    # 最后一列为标签（环数）

# 转换为 NumPy 数组
data_X = np.array(data_X, dtype=np.float32)
data_Y = np.array(data_Y, dtype=np.float32)
print('数据形状:', data_X.shape, data_Y.shape)
print('特征维度:', data_X.shape[1])

# 1.2 数据归一化（将特征缩放到 [0, 1]）
for i in range(data_X.shape[1]):
    _min = np.min(data_X[:, i])
    _max = np.max(data_X[:, i])
    data_X[:, i] = (data_X[:, i] - _min) / (_max - _min)

# 1.3 手动划分训练集和测试集（80%训练，20%测试）
def train_test_split_np(X, Y, test_size=0.2, random_state=None):
    """使用 NumPy 实现训练集和测试集划分"""
    if random_state is not None:
        np.random.seed(random_state)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    test_count = int(len(X) * test_size)
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]

    X_train = X[train_indices]
    Y_train = Y[train_indices]
    X_test = X[test_indices]
    Y_test = Y[test_indices]

    return X_train, X_test, Y_train, Y_test

X_train, X_test, y_train, y_test = train_test_split_np(data_X, data_Y, test_size=0.2, random_state=1)

# 拼接特征和标签方便批处理
train_data = np.concatenate((X_train, y_train), axis=1)
test_data = np.concatenate((X_test, y_test), axis=1)
print('训练集形状:', train_data.shape)
print('测试集形状:', test_data.shape)

# =====================
# 2. 网络配置
# =====================

# 初始化权重和偏置（8个特征 -> 1个输出）
weights = np.random.randn(8, 1).astype(np.float32)
bias = np.zeros((1, 1), dtype=np.float32)

# =====================
# 3. 网络训练与评估
# =====================

BATCH_SIZE = 50  # 小批量大小

def draw_train_process(epochs, costs):
    """绘制并保存训练损失曲线"""
    plt.figure()
    plt.plot(epochs, costs, color='red', label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Curve')
    plt.legend()
    plt.grid(True)
    plt.savefig('loss2.jpg')  # 保存损失曲线
    plt.show()

def train():
    """训练函数"""
    print('开始训练...')
    EPOCH_NUM = 100      # 迭代次数
    learning_rate = 0.0001
    epochs = []
    epoch_costs = []

    for epoch_id in range(EPOCH_NUM):
        # 打乱训练数据
        np.random.shuffle(train_data)
        # 划分为小批量
        mini_batches = [train_data[k:k + BATCH_SIZE] for k in range(0, len(train_data), BATCH_SIZE)]
        batch_costs = []

        for batch_id, data in enumerate(mini_batches):
            features = data[:, :8]  # 特征
            labels = data[:, -1:]   # 标签

            # 前向传播：预测值 y_pred = XW + b
            y_pred = np.dot(features, weights) + bias

            # 损失函数：均方误差 (MSE)
            cost = np.mean((y_pred - labels) ** 2)
            batch_costs.append(cost)

            # 反向传播：计算梯度
            dL_dy = 2 * (y_pred - labels) / BATCH_SIZE
            dL_dw = np.dot(features.T, dL_dy)  # 权重梯度
            dL_db = np.sum(dL_dy, axis=0, keepdims=True)  # 偏置梯度

            # 更新参数
            weights[:] -= learning_rate * dL_dw
            bias[:] -= learning_rate * dL_db

        # 记录每轮损失
        epoch_loss = np.mean(batch_costs)
        epochs.append(epoch_id)
        epoch_costs.append(epoch_loss)

        if epoch_id % 10 == 0:
            print(f"Epoch {epoch_id}: 平均损失 = {epoch_loss:.5f}")

    return epochs, epoch_costs

# 训练模型
epochs, epoch_costs = train()
draw_train_process(epochs, epoch_costs)

# 保存模型参数
np.savez('model2.npz', weights=weights, bias=bias)
print("模型已保存为 model2.npz")

# =====================
# 4. 模型预测与可视化
# =====================

def draw_infer_result(groud_truths, infer_results):
    """绘制并保存预测结果可视化"""
    plt.figure()
    plt.title('Abalone Age Prediction', fontsize=18)
    plt.xlabel('Ground Truth', fontsize=14)
    plt.ylabel('Predicted Age', fontsize=14)
    plt.scatter(groud_truths, infer_results, color='green', label='Predictions')
    plt.plot([min(groud_truths), max(groud_truths)],
             [min(groud_truths), max(groud_truths)],
             color='blue', linestyle='--', label='Ideal Prediction')
    plt.legend()
    plt.grid(True)
    plt.savefig('predict2.jpg')  # 保存预测图
    plt.show()

# 预测测试集
infer_features = test_data[:, :8]
infer_labels = test_data[:, -1]
infer_results = np.dot(infer_features, weights) + bias  # 线性回归预测

# 显示部分预测结果
INFER_BATCH_SIZE = 15
infer_results_part = infer_results[:INFER_BATCH_SIZE, 0]
groud_truths_part = infer_labels[:INFER_BATCH_SIZE]

for i in range(INFER_BATCH_SIZE):
    print(f"No.{i}: 预测值={infer_results_part[i]:.2f}, 真实值={groud_truths_part[i]:.2f}")

mean_loss = np.mean((infer_results_part - groud_truths_part) ** 2)
print(f"平均损失（测试集前 {INFER_BATCH_SIZE} 条）: {mean_loss:.4f}")

draw_infer_result(groud_truths_part, infer_results_part)

# =====================
# 5. 用户交互预测
# =====================

def predict_dataset(row):
    """预测数据集中某一行的结果"""
    if row < 0 or row >= len(data_X):
        print("输入行数超出范围！")
        return
    sample = data_X[row].reshape(1, -1)
    prediction = np.dot(sample, weights) + bias
    print(f"第 {row} 行数据预测年龄: {prediction[0][0]:.2f}")

def predict_user_input():
    """根据用户输入的8个特征进行预测"""
    try:
        input_str = input("请输入8个特征（用英文逗号分隔）: ")
        input_list = [float(x) for x in input_str.split(',')]
        if len(input_list) != 8:
            print("必须输入8个特征！")
            return

        # 归一化输入
        input_array = np.array(input_list, dtype=np.float32)
        for i in range(8):
            _min = np.min(data_X[:, i])
            _max = np.max(data_X[:, i])
            input_array[i] = (input_array[i] - _min) / (_max - _min)

        sample = input_array.reshape(1, -1)
        prediction = np.dot(sample, weights) + bias
        print(f"预测年龄: {prediction[0][0]:.2f}")
    except ValueError:
        print("输入格式错误，请输入数字！")

# =====================
# 6. 主程序交互入口
# =====================
if __name__ == '__main__':
    while True:
        print("\n请选择功能：")
        print("1：预测数据集中某行的年龄")
        print("2：预测用户输入的特征年龄")
        print("q：退出程序")
        choice = input("请输入 1 / 2 / q: ").strip()
        if choice == '1':
            row = int(input("请输入要预测的行号（0~{}）: ".format(len(data_X)-1)))
            predict_dataset(row)
        elif choice == '2':
            predict_user_input()
        elif choice == 'q':
            print("程序已退出。")
            break
        else:
            print("无效输入，请重新选择。")