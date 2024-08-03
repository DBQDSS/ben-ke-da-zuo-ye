import numpy as np

# 目标函数
def powell(x):
    return ((x[0] + 10 * x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2
            + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4)

# 目标函数的梯度
def grad_powell(x):
    return np.array([2 * (x[0] + 10 * x[1]) + 40 * (x[0] - x[3]) ** 3,
                    20 * (x[0] + 10 * x[1]) + 4 * (x[1] - 2 * x[2]) ** 3,
                    10 * (x[2] - x[3]) - 8 * (x[1] - 2 * x[2]) ** 3,
                    -10 * (x[2] - x[3]) - 40 * (x[0] - x[3]) ** 3])

# Armijo算法
def armijo(x, dk, c1=0.2, beta=0.5):
    alpha = 1
    while powell(x + alpha * dk) > powell(x) + c1 * alpha * np.dot(grad_powell(x), dk):
        alpha *= beta
    return alpha

# FR-CG算法
def FRCG(x0, max_iter=10000, tol=1e-19):
    """
    x0: 初始点
    max_iter: 最大迭代次数
    tol: 精度
    """
    x = x0
    k = 0
    d = - grad_powell(x)

    while k < max_iter:
        if np.linalg.norm(d) < tol:
            return x, powell(x), k

        # 求步长因子
        alpha = armijo(x, d)

        # 计算下一个迭代点
        x_new = x + alpha * d
        beta = (grad_powell(x_new).T @ grad_powell(x_new)) / (grad_powell(x).T @ grad_powell(x))
        d = -grad_powell(x_new) + beta * d

        # 更新点
        x = x_new
        k += 1 # 更新迭代次数
    return x, powell(x), k

# 初始点
x0 = np.array([3.0, -1, 0, 1])
x_star, f_min, k = FRCG(x0)
print("目标函数最优解：", x_star)
print("目标函数最小值：", f_min)
print("迭代次数：", k)