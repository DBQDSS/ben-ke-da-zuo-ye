import Romberg
import math
# 定义函数
def f(x):
    if x == 0:
        return 1
    return math.sin(x) / x

## 给定参数
a = 0  # 积分下限
b = math.pi / 2  # 积分上限
eps = 10 ** -15  # 给定精度

## 龙贝格求积分值
I = Romberg.romberg(f, a, b, eps)
print("\nI[f] = {:.10f}".format(I))