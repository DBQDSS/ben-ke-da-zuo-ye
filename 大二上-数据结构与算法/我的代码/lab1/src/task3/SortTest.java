package task3;

public class SortTest {
    // 使用指定的排序算法完成一次排序所需要的时间，单位是纳秒
    public static double time(SortAlgorithm alg, Double[] numbers){
        double start = System.nanoTime();
        alg.sort(numbers);
        double end = System.nanoTime();
        return end - start;
    }
    // 为了避免一次测试数据所造成的不公平，对一个实验完成T次测试，获得T次测试之后的平均时间
    public static double test(SortAlgorithm alg, Double[] numbers, int T)
    {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, numbers);
        return totalTime/T;
    }
    // 执行样例，仅供参考。
    // 由于测试数据的规模大小，算法性能，机器性能等因素，请同学们耐心等待每次程序的运行。
    public static void main(String[] args) {
        System.out.println("Time of 100&1000 datas");
        int[] dataLength = {100, 1000};
        double[] elapsedTime = new double[dataLength.length];
        SortAlgorithm alg = new QuickSortOfRecursion();
        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = test(alg, GenerateData.getRandomData(dataLength[i]), 5);
        for(double time: elapsedTime)
            System.out.printf("%6.4f ", time);
        System.out.println();


        QuickSortOfRecursion sorter = new QuickSortOfRecursion();
        Comparable[] arr = {10, 7, 8, 9, 1, 5};
        System.out.println("Original array");
        System.out.println("{10, 7, 8, 9, 1, 5}");
        sorter.sort(arr);
        System.out.println("Sorted array: ");
        sorter.show(arr);
    }
}
