# 导入相关包
import numpy as np
import math  # 绝对值函数
from scipy import integrate  # 求积分

# 求梯形值(返回用k阶复化梯形公式估计的积分)
def Trap(f, a, b, Iold, k):
    if k == 1:
        Inew = (f(a) + f(b)) * (b - a) / 2
    else:
        n = pow(2, k - 2) # 分点个数
        h = (b - a) / n  # 步长
        x = a + (h / 2)  # 第一步的中心点
        sum_k = 0
        for i in range(n):
            sum_k = sum_k + f(x)  # 求和
            x = x + h  # 下一个点
        Inew = (Iold + h * sum_k) / 2  # 递推公式
    return Inew


# 求加速值(运用理查森外推加速算法)
def Richardson(R, k):
    for i in range(k - 1, 0, -1):
        c = pow(2, 2 * (k - i))
        R[i] = (c * R[i + 1] - R[i]) / (c - 1)  # 龙贝格求积算法
    return R


# 龙贝格求积分法
def romberg(f, a, b, eps):
    T = {}  # 定义空字典
    k = 1 # 二分次数
    T[1] = Trap(f, a, b, 0.0, 1)
    former_R = T[1]
    while True:
        k += 1
        # 求梯形值
        T[k] = Trap(f, a, b, T[k - 1], k)
        # 求加速值
        T = Richardson(T, k)
        # 判断是否满足终止条件
        if abs(T[1] - former_R) < eps:
            return T[1]
        former_R = T[1]  # 最后一个值置为初始值