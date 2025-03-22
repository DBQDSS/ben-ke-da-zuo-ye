package task5;

import java.util.Random;

public class QuickSortDepthTest {
    public static void main(String[] args) {
        for (int n = 256; n <= 65536; n *= 2) {
            Comparable[] array = generateRandomArray(n);
            Quicksort quicksort = new Quicksort();
            quicksort.sort(array);
            int maxDepth = quicksort.getMaxDepth(); // 获取最大递归深度
            System.out.printf("Array size: %d, Max recursion depth: %d%n", n, maxDepth);
        }
    }

    private static Comparable[] generateRandomArray(int size) {
        Random random = new Random();
        Comparable[] array = new Comparable[size];
        for (int i = 0; i < size; i++) {
            array[i] = random.nextInt(10000); // 随机数范围在 0 到 9999
        }
        return array;
    }
}



