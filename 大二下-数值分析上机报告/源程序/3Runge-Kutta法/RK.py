import numpy as np
import math
import matplotlib.pyplot as plt


def f1(x, y1, y2, y3):
    df = y2
    return df


def f2(x, y1, y2, y3):
    df = y3
    return df


def f3(x, y1, y2, y3):
    df = y3 + y2 - y1 + 2 * x - 3
    return df


def RK4(x, y1, y2, y3, h):
    xarray, y1array, y2array, y3array = [], [], [], []
    while x <= 1.00:
        xarray.append(x)
        y1array.append(y1)
        y2array.append(y2)
        y3array.append(y3)
        x += h

        K_11 = f1(x, y1, y2, y3)
        K_21 = f2(x, y1, y2, y3)
        K_31 = f3(x, y1, y2, y3)
        K_12 = f1(x + h / 2, y1 + h / 2 * K_11, y2 + h / 2 * K_21, y3 + h / 2 * K_31)
        K_22 = f2(x + h / 2, y1 + h / 2 * K_11, y2 + h / 2 * K_21, y3 + h / 2 * K_31)
        K_32 = f3(x + h / 2, y1 + h / 2 * K_11, y2 + h / 2 * K_21, y3 + h / 2 * K_31)
        K_13 = f1(x + h / 2, y1 + h / 2 * K_12, y2 + h / 2 * K_22, y3 + h / 2 * K_32)
        K_23 = f2(x + h / 2, y1 + h / 2 * K_12, y2 + h / 2 * K_22, y3 + h / 2 * K_32)
        K_33 = f3(x + h / 2, y1 + h / 2 * K_12, y2 + h / 2 * K_22, y3 + h / 2 * K_32)
        K_14 = f1(x + h, y1 + h * K_13, y2 + h * K_23, y3 + h * K_33)
        K_24 = f2(x + h, y1 + h * K_13, y2 + h * K_23, y3 + h * K_33)
        K_34 = f3(x + h, y1 + h * K_13, y2 + h * K_23, y3 + h * K_33)

        y1 = y1 + (K_11 + 2 * K_12 + 2 * K_13 + K_14) * h / 6
        y2 = y2 + (K_21 + 2 * K_22 + 2 * K_23 + K_24) * h / 6
        y3 = y3 + (K_31 + 2 * K_32 + 2 * K_33 + K_34) * h / 6
    return xarray, y1array, y2array, y3array


def main():
    xarray, y1array, y2array, y3array = RK4(0, -1, 3, 2, 0.05)

    plt.figure('Runge Kutta numerical results')

    plt.subplot(221)
    plt.scatter(xarray, y1array, label='y1_scatter', s=1, color='blue', alpha=0.6)
    plt.legend()

    plt.subplot(222)
    plt.scatter(xarray, y2array, label='y2_scatter', s=1, color='blue', alpha=0.6)
    plt.legend()

    plt.subplot(223)
    plt.scatter(xarray, y3array, label='y3_scatter', s=1, color='blue', alpha=0.6)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()