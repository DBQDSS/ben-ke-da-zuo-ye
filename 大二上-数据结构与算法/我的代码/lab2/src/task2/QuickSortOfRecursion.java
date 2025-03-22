package task2;

import java.util.Stack;
public class QuickSortOfRecursion extends SortAlgorithm {

    // 覆盖父类的sort方法，输入一个可比较对象的数组
    @Override
    public void sort(Comparable[] objs) {
        // 创建一个范围的栈
        Stack<Range> stack = new Stack<>();
        // 将数组的索引范围入栈，索引开始为0，结束为数组长度-1
        stack.push(new Range(0, objs.length - 1));

        // 当栈不为空时执行循环
        while (!stack.isEmpty()) {
            // 弹出栈顶的范围项
            Range range = stack.pop();

            // 在索引起始值小于终止值时
            if(range.low < range.high){
                // 对数组范围内的元素进行分区，并返回新的基准点索引
                int pivot = partition(objs, range.low, range.high);
                // 将基准点左侧的范围入栈
                stack.push(new Range(range.low,pivot - 1));
                // 将基准点右侧的范围入栈
                stack.push(new Range(pivot + 1, range.high));
            }
        }
    }

    // 将数组的一部分以对象高位为划分点分为两部分，返回分区后的基准点索引
    private int partition(Comparable[] objs,int low,int high){
        // 将最后一个对象作为基准点
        Comparable pivot=objs[high];
        int i=low-1;
        // 从索引 low 开始至 high-1结束，针对数组每个元素
        for (int j = low; j < high; j++){
            // 若当前元素小于等于基准点值
            if(less(objs[j], pivot) || equals(objs[j], pivot)){
                i++;
                // 交换 i 和 j 位置的元素
                exchange(objs, i, j);
            }
        }
        // 交换 i+1 和 high 位置的元素
        exchange(objs, i + 1, high);
        return i + 1;
    }

    // 定义Range静态内部类，保存索引范围
    static class Range{
        // low, high，分别代表底部和顶部
        int low,high;
        // 构造函数，用于新建一个范围
        public Range(int low,int high){
            this.high = high;
            this.low = low;
        }
    }

    // 测试
    public static void main(String[] args) {

        QuickSortOfRecursion sorter = new QuickSortOfRecursion();
        Comparable[] arr = {12, -7, 26, 5, -14, 30, 21, -9, 10, -28, 15, 23, -6, 19, -4};

        // 打印原始数组
        System.out.println("原始数组为："+"[12, -7, 26, 5, -14, 30, 21, -9, 10, -28, 15, 23, -6, 19, -4]");
        // 使用sorter对象对数组进行排序
        sorter.sort(arr);
        // 打印排序后的数组
        System.out.println("排序后的数组为：");
        sorter.show(arr);
    }
}
