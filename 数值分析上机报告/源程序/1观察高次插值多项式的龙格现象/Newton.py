import sympy as sp
import numpy as np
from matplotlib import pyplot as plt

class Newton:
    def __init__(self, N):
        self.n = N
        self.DataX = np.linspace(-1, 1, N) # 插值点，-1到1之间的 N 个点等距分布
        self.x = sp.symbols('x')
        self.Px = sp.expand(self.generatePx(self.DataX)) # 计算牛顿插值多项式
        self.draw() # 绘制函数图像

    # 被插函数
    def f(self, X):
        return 1 / (1 + 25 * X ** 2)

    # 牛顿插值函数
    def ff(self, X=list()):
        if len(X) < 2:
            raise ValueError('X\'s length must be bigger than 2')
        ans = 0
        for i in range(len(X)):
            temp = 1.0
            for j in range(len(X)):
                if j == i:
                    continue
                temp *= (X[i] - X[j])
            ans += (self.f(X[i]) / temp)
        return ans

    # 绘图
    def draw(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        X = np.linspace(-1, 1, 100)

        TargetY = self.f(X)
        GetY = [self.Px.subs(self.x, i) for i in X]

        # 标签，此处为 N = 10 的情况
        plt.plot(X, TargetY, label=r'$\frac{1}{1 + 25 x^2}$') # 被插函数图象
        plt.plot(X, GetY, label='$N_{10}(x)$') # 牛顿插值多项式图像
        plt.legend()
        plt.show()

    # 递归生成牛顿插值多项式
    def generatePx(self, DataX):
        ans = self.f(DataX[0])
        if len(DataX) == 1:
            return ans
        else:
            temp = 1
            for i in range(len(DataX) - 1):
                temp *= (self.x - DataX[i])
                ans += self.ff(DataX[:i + 2]) * temp
            return ans
