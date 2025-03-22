import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
import Newton
import cubic

def f(X):
    return 1 / (1 + 25 * X ** 2)

def ff(X=list()):
    if len(X) < 2:
        raise ValueError('X\'s length must be bigger than 2')
    ans = 0
    for i in range(len(X)):
        temp = 1.0
        for j in range(len(X)):
            if j == i:
                continue
            temp *= (X[i] - X[j])
        ans += (f(X[i]) / temp)
    return ans

def generatePx(DataX):
    ans = f(DataX[0])
    if len(DataX) == 1:
        return ans
    else:
        temp = 1
        for i in range(len(DataX) - 1):
            temp *= (x - DataX[i])
            ans += ff(DataX[:i + 2]) * temp
        return ans

if __name__ == '__main__':
    x = sp.symbols('x')

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    X = np.linspace(-1, 1, 100)

    TargetY = f(X)
    plt.plot(X, TargetY, label=r'$\frac{1}{1+25x^2}$')

    DataX1 = np.linspace(-1, 1, 5)  # 插值点
    Px1 = sp.expand(generatePx(DataX1))
    GetY1 = [Px1.subs(x, i) for i in X]
    plt.plot(X, GetY1, label='$N_{5}(x)$')

    DataX2 = np.linspace(-1, 1, 10)  # 插值点
    Px2 = sp.expand(generatePx(DataX2))
    GetY2 = [Px2.subs(x, i) for i in X]
    plt.plot(X, GetY2, label='$N_{10}(x)$')

    x = np.linspace(-1, 1, 10)
    y = f(x)
    ncs = cubic.Natural_cubic_spline(x, y)
    ncs.fit()
    xn = np.linspace(-1, 1, 100)
    yn = ncs.eval(xn)
    plt.scatter(x, y)
    plt.plot(xn, yn, label='$S_{10}(x)$')

    plt.legend()
    plt.show()