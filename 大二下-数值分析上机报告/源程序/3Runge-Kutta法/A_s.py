# 解析解 Analytical solution
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

# 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 显示减号
plt.rcParams['axes.unicode_minus'] = False

def f(x):
    return x * sp.exp(x) + 2 * x - 1

def ff(xn):
    yn = np.zeros(len(xn))
    for i in range(len(xn)):
        yn[i] = f(xn[i])
    return yn

xn = np.linspace(0, 1, 500)
yn = ff(xn)

# 绘制图像，设置 color 为 red，线宽度是 1，线的样式是 --
plt.plot(xn, yn, color='red', linewidth=1.0, label="解析解")
plt.legend()
plt.show()