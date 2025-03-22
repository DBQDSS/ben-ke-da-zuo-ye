package task2;

import java.util.Stack;

public class HanoiTowerNonRecursive {
    // 定义从 '0','A','B','C' 对应的字符数组
    private static char[] s = {'0', 'A', 'B', 'C'};
    // 创建一个堆栈数组来存放盘子
    private static Stack<Integer>[] a = new Stack[4];

    public static void main(String[] args) {
        // 为每个堆栈创建空间
        for (int i = 0; i < 4; i++)
            a[i] = new Stack<>();
        System.out.println("非递归方法解决汉诺塔问题：");
        // 解决汉诺塔问题的主调方法
        solveHanoiTower(15);
    }

    // 移动盘子的方法
    private static void move(int now, int next) {
        // 将当前盘子从一个塔移到另一个塔
        a[next].push(a[now].peek());
        // 输出移动的步骤
        System.out.printf("%d号盘：%c --> %c\n", a[now].peek(), s[now], s[next]);
        // 移除当前的塔顶盘子
        a[now].pop();
    }

    // 汉诺塔的解决方法
    private static void solveHanoiTower(int n) {
        // 依次将n个盘子从大到小压入第一个塔
        for (int i = n; i > 0; i--)
            a[1].push(i);
        // 当盘子数为奇数时，调整初始的塔的顺序
        if (n % 2 == 1) {
            s[2] = 'C';
            s[3] = 'B';
        }

        // 当所有的盘子都移动到目标塔时，结束循环
        while (true) {
            int next = 0;
            // 找到最小盘子并移到下一个塔
            for (int i = 1; i <= 3; i++)
                if (!a[i].isEmpty() && a[i].peek() == 1) {
                    next = i == 3 ? 1 : i + 1;
                    move(i, next);
                    break;
                }
            // 当所有盘子都移到了目标塔，则跳出循环
            if (a[2].size() == n || a[3].size() == n)
                break;

            // 记录非当前的两个塔
            int other1 = 0, other2 = 0;
            switch (next) {
                case 1: {
                    other1 = 2;
                    other2 = 3;
                    break;
                }
                case 2: {
                    other1 = 3;
                    other2 = 1;
                    break;
                }
                case 3: {
                    other1 = 1;
                    other2 = 2;
                    break;
                }
            }

            // 移动非当前塔中较小的盘子到较大的塔
            if (a[other1].isEmpty())
                move(other2, other1);
            else if (a[other2].isEmpty())
                move(other1, other2);
            else {
                if (a[other1].peek() < a[other2].peek())
                    move(other1, other2);
                else move(other2, other1);
            }
        }
    }
}