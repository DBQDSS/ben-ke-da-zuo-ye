import numpy as np

# 目标函数
def f(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

# 目标函数的梯度
def grad_f(x):
    return np.array([- 400 * (x[1] - x[0] ** 2) * x[0] - 2 * (1 - x[0]), 200 * (x[1] - x[0] ** 2)])

# 海森矩阵
def hessian(x):
    x1 = x[0]
    x2 = x[1]
    return np.array([[ - 400 * (x2 - 3 * x1 ** 2) + 2, - 400 * x1],
                     [- 400 * x1 , 200]])
# 牛顿法
def newton(x0, max_iter=10000, tol=1e-10):
    """
    x0: 初始点
    max_iter: 最大迭代次数
    tol: 精度
    """
    x = x0
    k = 0 # 计数：迭代次数
    while k < max_iter:
        g = grad_f(x)
        G = hessian(x) # 海森阵
        x_new = x - np.squeeze(np.linalg.inv(G) @ g)
        if np.linalg.norm(g) < tol:
            break
        x = x_new # 更新点
        k += 1 # 更新迭代次数
    return x, f(x), k

# 初始点
x0 = np.array([-1.2, 1])
x_star, f_min, k = newton(x0)
print("目标函数最优解：", x_star)
print("目标函数最小值：", f_min)
print("迭代次数：", k)

