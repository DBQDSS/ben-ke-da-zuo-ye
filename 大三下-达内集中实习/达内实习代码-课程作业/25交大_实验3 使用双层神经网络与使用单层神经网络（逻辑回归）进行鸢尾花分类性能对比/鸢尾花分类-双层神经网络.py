import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report

# 设置中文显示
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 定义双层神经网络模型
class IrisDoubleLayerNetwork(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=8, output_dim=3):
        super(IrisDoubleLayerNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def load_and_preprocess_data():
    """加载并预处理鸢尾花数据集"""
    df = pd.read_csv('Iris.txt', header=None,
                     names=['sepal_length', 'sepal_width',
                            'petal_length', 'petal_width', 'species'])

    # 标签映射为数字
    species_mapping = {
        'Iris-setosa': 0,
        'Iris-versicolor': 1,
        'Iris-virginica': 2
    }
    df['label'] = df['species'].map(species_mapping)

    # 划分特征和标签
    X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
    y = df['label'].values

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # 特征标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 转换为PyTorch张量
    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    return (X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor,
            scaler, df, X, y, X_test, y_test)  # 返回原始测试集特征

def train_model(X_train, y_train, X_test, y_test, epochs=1000):
    """训练双层神经网络模型"""
    model = IrisDoubleLayerNetwork()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        # 训练模式
        model.train()
        optimizer.zero_grad()

        # 前向传播
        outputs = model(X_train)
        loss = criterion(outputs, y_train)

        # 反向传播和优化
        loss.backward()
        optimizer.step()

        # 记录训练损失
        train_losses.append(loss.item())

        # 测试模式
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test)
            test_loss = criterion(test_outputs, y_test)
            test_losses.append(test_loss.item())

        # 每100轮打印一次信息
        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Train Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')

    # 保存模型
    torch.save(model.state_dict(), 'model2.pth')
    print("模型已保存为 model2.pth")
    return model, train_losses, test_losses

def plot_loss_curve(train_losses, test_losses):
    """绘制训练和测试损失曲线"""
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(train_losses) + 1), train_losses, label='训练损失')
    plt.plot(range(1, len(test_losses) + 1), test_losses, label='测试损失')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('训练和测试损失曲线')
    plt.legend()
    plt.grid(True)
    plt.savefig('loss2.jpg')
    print("损失曲线已保存为 loss2.jpg")
    plt.close()

def visualize_model_performance(model, X_test, y_test, original_X_test):
    """模型性能可视化：测试集预测结果的特征对分布图（替代原分布曲线）"""
    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        _, predicted = torch.max(outputs.data, 1)  # 预测类别（数字标签）

    # 1. 混淆矩阵（保留原逻辑）
    cm = confusion_matrix(y_test.numpy(), predicted.numpy())
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Setosa', 'Versicolor', 'Virginica'],
                yticklabels=['Setosa', 'Versicolor', 'Virginica'])
    plt.xlabel('预测标签')
    plt.ylabel('真实标签')
    plt.title('混淆矩阵')
    plt.savefig('confusion_matrix2.jpg')
    plt.close()
    print("混淆矩阵已保存为 confusion_matrix2.jpg")

    # 2. 测试集预测结果的特征对分布图（核心修改：仿造参考图的pairplot）
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    species_names = ['Setosa', 'Versicolor', 'Virginica']
    predicted_names = [species_names[i] for i in predicted.numpy()]  # 转换为类别名称

    # 构建DataFrame：原始特征 + 预测类别
    test_pred_df = pd.DataFrame(original_X_test, columns=features)
    test_pred_df['predicted_species'] = predicted_names

    # 绘制pairplot：对角线KDE分布，非对角线散点，按预测类别着色
    g = sns.pairplot(
        test_pred_df,
        hue='predicted_species',  # 按预测类别区分颜色
        vars=features,  # 仅展示4个特征
        diag_kind='kde',  # 对角线用KDE曲线（参考图的分布曲线）
        markers=['o', 's', 'D'],  # 不同类别用不同标记（圆、方形、菱形）
        palette='colorblind',  # 色盲友好配色
        height=2.5,  # 调整子图大小
        aspect=1  # 子图宽高比
    )
    g.fig.suptitle('测试集预测结果：特征分布与关联', y=1.02)  # 标题置顶
    plt.savefig('predicted_feature_pairplot2.jpg', bbox_inches='tight')
    plt.close()
    print("测试集预测结果的特征对图已保存为 predicted_feature_pairplot2.jpg")

    # 3. 分类报告（保留原逻辑）
    print("\n分类报告:")
    print(classification_report(y_test.numpy(), predicted.numpy(),
                                target_names=species_names))

def predict_single_from_test(model, X_test, y_test, original_X_test):
    """从测试集中选择数据进行预测"""
    try:
        row_num = int(input("请输入要测试的行数 (0-29): "))
        if row_num < 0 or row_num >= len(X_test):
            print(f"错误：行数超出范围！测试集共有 {len(X_test)} 行数据，请输入 0-{len(X_test) - 1} 之间的数")
            return

        sample = X_test[row_num].unsqueeze(0)
        true_label = y_test[row_num].item()
        with torch.no_grad():
            output = model(sample)
            _, predicted = torch.max(output.data, 1)
            predicted_label = predicted.item()

        # 获取原始特征值
        sample_original = original_X_test[row_num]
        label_map = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        print("\n===== 测试集单条数据预测 =====")
        print(f"测试数据行号: {row_num}")
        print(f"特征值: 花萼长度={sample_original[0]:.2f}cm, 花萼宽度={sample_original[1]:.2f}cm, "
              f"花瓣长度={sample_original[2]:.2f}cm, 花瓣宽度={sample_original[3]:.2f}cm")
        print(f"真实类别: {label_map[true_label]}")
        print(f"预测类别: {label_map[predicted_label]}")
        print("预测概率分布:")
        probs = torch.softmax(output, dim=1).numpy()[0]
        for i, class_name in enumerate(label_map.values()):
            print(f"  {class_name}: {probs[i]:.4f}")
        print("===========================")
    except ValueError:
        print("输入错误，请输入有效的整数行数！")

def predict_user_input(model, scaler):
    """用户输入特征进行预测"""
    try:
        print("\n请输入鸢尾花的四个特征值（单位：cm）")
        sepal_length = float(input("花萼长度: "))
        sepal_width = float(input("花萼宽度: "))
        petal_length = float(input("花瓣长度: "))
        petal_width = float(input("花瓣宽度: "))

        # 构建输入向量并标准化
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        input_scaled = scaler.transform(input_data)
        input_tensor = torch.tensor(input_scaled, dtype=torch.float32)

        # 预测
        model.eval()
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output.data, 1)
            predicted_label = predicted.item()

        label_map = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        print(f"\n预测结果: 该鸢尾花属于 {label_map[predicted_label]}")
    except ValueError:
        print("输入错误，请确保输入的是数字！")

def main():
    # 加载和预处理数据
    X_train, y_train, X_test, y_test, scaler, df, _, _, original_X_test, _ = load_and_preprocess_data()

    # 训练模型
    model, train_losses, test_losses = train_model(X_train, y_train, X_test, y_test)

    # 绘制损失曲线
    plot_loss_curve(train_losses, test_losses)

    # 模型性能可视化（传入原始测试集特征）
    visualize_model_performance(model, X_test, y_test, original_X_test)

    # 交互菜单
    while True:
        print("\n===== 鸢尾花分类预测系统 =====")
        print("1. 输入行数从测试集中选择数据进行预测")
        print("2. 输入特征值进行预测")
        print("q. 退出系统")
        choice = input("请选择操作 (1/2/q): ")

        if choice == '1':
            predict_single_from_test(model, X_test, y_test, original_X_test)
        elif choice == '2':
            predict_user_input(model, scaler)
        elif choice == 'q':
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入！")

if __name__ == "__main__":
    main()