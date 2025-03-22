import numpy as np
import matplotlib.pyplot as plt

class Natural_cubic_spline:
    def __init__(self, x, y):
        self.x = np.array(x)  # n个点的x值
        self.y = np.array(y)  # n个点的y值
        self.h = self.x[1:] - self.x[:-1]  # n-1个值
        self.dy = self.y[1:] - self.y[:-1] # n-1个值

    @staticmethod
    def f(x):
        return 1 / (1 + 25 * x ** 2)

    def gen_equation(self):
        v1 = self.h.copy() # v1表示对H矩阵对角线左侧的值
        v1[-1] = 0

        v2 = 2*np.ones(len(self.x)) # v2表示对H矩阵对角线值
        v2[1:-1] = 2*(self.h[:-1] + self.h[1:])

        v3 = self.h.copy() # v3表示对H矩阵对角线右侧的值
        v3[0] = 0

        H = np.diag(v1, -1) + np.diag(v2, 0) + np.diag(v3, 1)

        d = np.zeros(len(self.x))
        d[1:-1] = 6 * (self.dy[1:] / self.h[1:] - self.dy[:-1] / self.h[:-1])

        return H, d

    def solve_m(self):
        H, d = self.gen_equation()
        m = np.linalg.solve(H, d)
        return m

    def fit(self):
        m = self.solve_m()
        ai = self.y[:-1]
        bi = (self.dy / self.h - 1/2 * self.h * m[:-1] - 1/6 * self.h * (m[1:] - m[:-1]))
        ci = m[:-1] / 2
        di = 1/6 / self.h * (m[1:] - m[:-1])
        coef = np.array([ai, bi, ci, di]).T
        self.coef = coef

    def eval(self, xn):
        yn = np.zeros(len(xn))
        for i in range(len(xn)):
            xn_idx = np.where(self.x <= xn[i])[0][-1]
            if xn_idx < len(self.coef):
                a, b, c, d = self.coef[xn_idx]
                yn[i] = a + b * (xn[i] - self.x[xn_idx]) + c * (xn[i] - self.x[xn_idx]) ** 2 + d * (xn[i] - self.x[xn_idx]) ** 3
            else:
                a, b, c, d = self.coef[-1]
                yn[i] = a + b * (xn[i] - self.x[-1]) + c * (xn[i] - self.x[-1]) ** 2 + d * (xn[i] - self.x[-1]) ** 3
        return yn

# 随便创建一些节点
x = np.linspace(-1, 1, 100)
y = Natural_cubic_spline.f(x)
plt.plot(x,Natural_cubic_spline.f(x),label=r'$\frac{1}{1 + 25 x^2}$')

x = np.linspace(-1, 1, 10)
y = Natural_cubic_spline.f(x)
plt.scatter(x, y)

ncs = Natural_cubic_spline(x, y)
ncs.fit()
xn = np.linspace(-1, 1, 100)
yn = ncs.eval(xn)
plt.scatter(x, y)
plt.plot(xn, yn,label='$S_{10}(x)$')

plt.legend()
plt.show()