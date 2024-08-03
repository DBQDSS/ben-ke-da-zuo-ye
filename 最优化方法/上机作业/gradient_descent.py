import numpy as np

# 目标函数
def f(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

# 目标函数的梯度
def grad_f(x):
    return np.array([- 400 * (x[1] - x[0] ** 2) * x[0] - 2 * (1 - x[0]), 200 * (x[1] - x[0] ** 2)])

# Armijo算法
def armijo(x, dk, c1=0.2, beta=0.5):
    alpha = 1
    while f(x + alpha * dk) > f(x) + c1 * alpha * np.dot(grad_f(x), dk):
        alpha *= beta
    return alpha

# 最速下降法
def gradient_descent(x0, max_iter=10000, tol=1e-12):
    """
    x0: 初始点
    max_iter: 最大迭代次数
    tol: 精度
    """
    x = x0
    k = 0 # 计数：迭代次数
    while k < max_iter:
        g = grad_f(x)
        d = - g
        # 求步长因子alpha
        alpha = armijo(x, d)
        x_new = x + alpha * d
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new # 更新点
        k += 1 # 更新迭代次数
    return x, f(x), k

# 初始点
x0 = np.array([-1.2, 1])
x_star, f_min, k = gradient_descent(x0)
print("目标函数最优解：", x_star)
print("目标函数最小值：", f_min)
print("迭代次数：", k)