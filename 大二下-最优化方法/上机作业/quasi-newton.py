import numpy as np

def powell(x):
    return ((x[0] + 10 * x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2
            + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4)


def grad_powell(x):
    return np.array([2 * (x[0] + 10 * x[1]) + 40 * (x[0] - x[3]) **3,
                    2 * (x[0] + 10 * x[1]) + 4 * (x[1] - 2 * x[2]) **3,
                    10 * (x[2] - x[3]) - 8 * (x[1] - 2 * x[2]) **3,
                    -10 * (x[2] - x[3]) - 40 * (x[0] - x[3]) **3]).reshape(1,-1).T

# BFGS算法
def bfgs_update(B, s, y):
    return B + (y @ y.T) / (y.T @ s) - (B @ s @ s.T @ B) / (s.T @ B @ s)

# Armijo算法
def armijo(x, dk, c1=0.2, beta=0.5):
    alpha = 1
    while powell(x + alpha * dk) > powell(x) + c1 * alpha * np.dot(grad_powell(x).T, dk):
        alpha *= beta
    return alpha


def quasi_newton_method(x0, max_iter=10000, tol=1e-19):
    """
    x0: 初始点
    tol: 收敛阈值
    max_iter: 最大迭代次数
    """
    # 转为列向量
    x = x0.reshape(1,-1).T
    B = np.eye(4)  # 初始海森矩阵近似为单位矩阵
    g = grad_powell(x)

    k = 0  # 计数
    while k < max_iter:
        # 检查收敛性
        if np.linalg.norm(g) < tol:
            break

        # 计算搜索方向
        d = - np.linalg.inv(B) @ g

        # 求步长因子 alpha
        alpha = armijo(x, d)
        x_new = x + alpha * d
        g_new = grad_powell(x_new)

        # 计算s和y
        s = x_new - x
        y = g_new - g

        # BFGS校正更新B
        B = bfgs_update(B, s, y)

        # 更新x和g
        x = x_new
        g = g_new

        k += 1
    return x, powell(x), k

# 初始点
x0 = np.array([3,-1,0,1])
# 使用拟牛顿法求解
x_star, f_min, k= quasi_newton_method(x0)
# 转为行向量
x_star = x_star.T.reshape(4)
print("目标函数最优解：", x_star)
print("目标函数最小值：", f_min)
print("迭代次数：", k)