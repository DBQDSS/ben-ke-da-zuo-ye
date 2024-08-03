import numpy as np
import matplotlib.pyplot as plt
import math
import RK
import A_s
from pylab import mpl

# 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 显示减号
plt.rcParams['axes.unicode_minus'] = False

# 数值解
xarray, y1array, y2array, y3array = RK.RK4(0, -1, 3, 2, 0.05)
plt.scatter(xarray, y1array, label='数值解', color='blue', marker='o', s=15, alpha=0.5, edgecolors='black')

# 解析解
xn = np.linspace(0, 1, 500)
yn = A_s.ff(xn)
plt.plot(xn, yn, color='red', linewidth=1.0, label='解析解')

plt.legend()
plt.show()

# zn = log10( |解析解 - 数值解| )，共19个元素
# 去掉初始点（重合）
zn = np.zeros(len(xarray)-1)
for i in range(len(xarray)-1):
    zn[i] = math.log10( math.fabs(A_s.f(xarray[i+1]) - y1array[i+1]))

# 去点
xarray.pop(0)
plt.scatter(xarray, zn, label='分点', color='blue', marker='o', s=15, alpha=0.5, edgecolors='black')
plt.plot(xarray, zn, color='red', linewidth=1.0, label='log10(|解析解-数值解|)')

plt.legend()
plt.show()