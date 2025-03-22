package task5;

public class Quicksort extends SortAlgorithm {
    public int gap;
    private int depth; // 用于追踪递归深度
    private int maxDepth; // 记录最大递归深度

    public void sort(Comparable[] objs) {
        depth = 0; // 初始化递归深度
        maxDepth = 0; // 初始化最大递归深度
        qsort(objs, 0, objs.length - 1);
    }

    public void qsort(Comparable[] objs, int i, int j) {

        depth++; // 进入递归，深度加 1
        if (depth > maxDepth) {
            maxDepth = depth; // 更新最大递归深度
        }
        System.out.println("Current depth: " + depth); // 打印当前深度

        int pivoindex = findpivot(objs, i, j);
        exchange(objs, pivoindex, j);
        int k = partition(objs, i - 1, j, objs[j]);
        exchange(objs, k, j);

        if ((k - i) > 1) qsort(objs, i, k - 1);
        if ((j - k) > 1) qsort(objs, k + 1, j);

        depth--; // 递归返回，深度减 1
    }

    public int findpivot(Comparable[] objs, int i, int j) {
        if (less(objs[i], objs[j]) && less(objs[(i + j) / 2], objs[i])) {
            return i;
        } else if (less(objs[j], objs[i]) && less(objs[(i + j) / 2], objs[j])) {
            return j;
        } else {
            return (i + j) / 2;
        }
    }

    public int partition(Comparable[] objs, int i, int j, Comparable pivot) {
        do {
            while (less(objs[++i], pivot)) ;
            while ((j != 0) && (less(pivot, objs[--j]))) ;
            exchange(objs, i, j);
        } while (i < j);

        exchange(objs, i, j);
        return i;
    }

    // 返回最大递归深度
    public int getMaxDepth() {
        return maxDepth; // 返回最大深度
    }

    // 重置递归深度
    public void resetDepth() {
        maxDepth = 0; // 返回最大深度
    }
}
