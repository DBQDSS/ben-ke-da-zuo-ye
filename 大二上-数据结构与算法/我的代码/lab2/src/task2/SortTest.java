package task2;

public class SortTest {
    // 使用指定的排序算法完成一次排序所需要的时间，单位是纳秒
    public static double time(SortAlgorithm alg, Double[] numbers) {
        double start = System.nanoTime();
        alg.sort(numbers);
        double end = System.nanoTime();
        return end - start;
    }

    // 为了避免一次测试数据所造成的不公平，对一个实验完成 T 次测试，获得 T 次测试之后的平均时间
    public static double test(SortAlgorithm alg, Double[] numbers, int T) {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, numbers);
        return totalTime/T;
    }

    public static void main(String[] args) {

        QuickSortOfRecursion sorter = new QuickSortOfRecursion();
        Comparable[] arr = {10, 7, 8, 9, 1, 5};
        System.out.println("Original array");
        System.out.println("{10, 7, 8, 9, 1, 5}");
        sorter.sort(arr);
        System.out.println("Sorted array: ");
        sorter.show(arr);

        System.out.println("Time of 100&1000&10000 datas");
        int[] dataLength = {100, 1000};
        double[] elapsedTime = new double[dataLength.length];
        SortAlgorithm alg = new QuickSortOfRecursion();

        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = test(alg, GenerateData.getRandomData(dataLength[i]), 20);
        for(double time: elapsedTime)
            System.out.printf("%6.4f ", time);
        System.out.println();
    }
}
