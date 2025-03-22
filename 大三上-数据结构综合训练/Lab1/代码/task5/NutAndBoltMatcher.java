package task5;

import java.util.Arrays;

public class NutAndBoltMatcher {
    // 模拟 match 函数
    private static int match(int nut, int bolt) {
        if (nut == bolt) return 0;
        if (nut > bolt) return 1;
        return -1;
    }

    public static void matchNutsAndBolts(int[] nuts, int[] bolts, int low, int high) {
        if (low < high) {
            // 使用 nuts[low] 作为基准，对 bolts 进行划分
            int pivot = partition(bolts, low, high, nuts[low]);
            // 使用对应的 bolt 对 nuts 进行划分
            partition(nuts, low, high, bolts[pivot]);

            // 递归处理左右两部分
            matchNutsAndBolts(nuts, bolts, low, pivot - 1);
            matchNutsAndBolts(nuts, bolts, pivot + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high, int pivot) {
        int i = low;
        for (int j = low; j <= high; j++) {
            int compareResult = match(arr[j], pivot);
            if (compareResult == -1) {
                // 交换元素
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
                i++;
            }
        }
        // 将 pivot 放到正确位置
        for (int k = low; k <= high; k++) {
            if (match(arr[k], pivot) == 0) {
                int temp = arr[k];
                arr[k] = arr[i];
                arr[i] = temp;
                break;
            }
        }
        return i;
    }

    public static void main(String[] args) {
        int[] nuts = {6, 5, 3, 1, 4, 2};
        int[] bolts = {2, 4, 6,1, 3, 5};

        System.out.println("Before matching:");
        System.out.println("Nuts: " + Arrays.toString(nuts));
        System.out.println("Bolts: " + Arrays.toString(bolts));

        matchNutsAndBolts(nuts, bolts, 0, nuts.length - 1);

        System.out.println("\nAfter matching:");
        System.out.println("Nuts: " + Arrays.toString(nuts));
        System.out.println("Bolts: " + Arrays.toString(bolts));
    }
}
