package task2;

import java.util.Stack;

public class HanoiTower {

    // 定义三个栈，分别表示三个塔
    Stack<Integer> A = new Stack<Integer>();
    Stack<Integer> B = new Stack<Integer>();
    Stack<Integer> C = new Stack<Integer>();

    // 移动盘子的方法
    public void move(int n, String from, String buffer, String to) {
        if (n <= 0) // 如果没有盘子需要移动，则直接返回
            return;
        move(n-1, from, to, buffer); // 把上面的 n-1 个盘子，借助 to，移动到 buffer 上
        moveTop(from, to); // 把最后一个盘子从 from 移动到 to
        move(n-1, buffer, from, to); // 最后把 buffer 上的 n-1 个盘子，借助 from，移动到 to 上
    }

    // 移动栈顶盘子的方法
    private void moveTop(String from, String to) {
        int disc = 0;
        if (from.equals("A")) // 如果应该从A塔取盘子
            disc = A.pop(); // 从A塔的顶部取出盘子
        else if (from.equals("B")) // 如果应该从B塔取盘子
            disc = B.pop();  // 从B塔的顶部取出盘子
        else if (from.equals("C")) // 如果应该从C塔取盘子
            disc = C.pop();  // 从C塔的顶部取出盘子

        if (to.equals("A")) // 如果盘子应该放到A塔
            A.push(disc); // 把盘子放到A塔的顶部
        else if (to.equals("B")) // 如果盘子应该放到B塔
            B.push(disc);  // 把盘子放到B塔的顶部
        else if (to.equals("C")) // 如果盘子应该放到C塔
            C.push(disc);  // 把盘子放到C塔的顶部

        System.out.println(disc + "号盘：" + from + "-->" + to); // 打印盘子移动信息
    }

    // 汉诺塔的主方法
    public void hanoi(int n) {
        for(int i = n; i >= 1; i--) {
            // 把所有的盘子按大小顺序（从小到大）放入A塔
            A.push(i);
        }

        move(n, "A", "B", "C"); // 通过递归移动把A塔的盘子移动到C塔
    }

    // 测试方法
    public static void main(String[] args) {
        HanoiTower h = new HanoiTower(); // 实例化HanoiTower类
        System.out.println("用递归的方式解决汉诺塔问题：");
        h.hanoi(15); // 调用hanoi方法解决3个盘子的汉诺塔问题
    }
}