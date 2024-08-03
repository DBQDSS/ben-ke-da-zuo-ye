package sort;

import static java.util.Arrays.sort;

public class SortTest {
    // 使用指定的排序算法完成一次排序所需要的时间，单位是纳秒
    public static double time(SortAlgorithm alg, Double[] numbers){
        double start = System.nanoTime();
        alg.sort(numbers);
        double end = System.nanoTime();
        return end - start;
    }
    // 为了避免一次测试数据所造成的不公平，对一个实验完成T次测试，获得T次测试之后的平均时间
    public static double testForSortedRepeat(SortAlgorithm alg, int length, int T,double scale)
    {
        Double[] temparr=GenerateData.getSortedRepeat(length,scale);
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, temparr);
        return totalTime/T;
    }

    public static double testForInversedRepeat(SortAlgorithm alg, int length, int T,double scale)
    {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, GenerateData.getInversedRepeat(length,scale));
        return totalTime/T;
    }

    public static double testForRandomRepeat(SortAlgorithm alg, int length, int T,double scale)
    {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, GenerateData.getRandomRepeat(length,scale));
        return totalTime/T;
    }
    public static double testForAcsending(SortAlgorithm alg, int length, int T)
    {
        Double[] temparr=GenerateData.getSortedData(length);
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, temparr);
        return totalTime/T;
    }

    public static double testForDecsending(SortAlgorithm alg, int length, int T)
    {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, GenerateData.getInversedData(length));
        return totalTime/T;
    }

    public static double testForRandom(SortAlgorithm alg,int length, int T){
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, GenerateData.getRandomData(length));
        return totalTime/T;
    }
    public static double testForRandomSome(SortAlgorithm alg,int length, int T){
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, GenerateData.getRandomSome(length));
        return totalTime/T;
    }
    public static double testForDecsendingSome(SortAlgorithm alg, int length, int T)
    {
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg,GenerateData.getInversedSome(length));
        return totalTime/T;
    }
    public static double testForAcsendingSome(SortAlgorithm alg, int length, int T)
    {
        Double[] temparr=GenerateData.getSortedSome(length);
        double totalTime = 0;
        for(int i = 0; i < T; i++)
            totalTime += time(alg, temparr);
        return totalTime/T;
    }
    // 执行样例，仅供参考。
    // 由于测试数据的规模大小，算法性能，机器性能等因素，请同学们耐心等待每次程序的运行。
    public static void main(String[] args) {
        int[] dataLength = {1000, 1000,1000};
        double[] elapsedTime = new double[dataLength.length];

        SortAlgorithm alg = new Insertion();

        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = testForRandom(alg, dataLength[i], 5);

        for(double time: elapsedTime)
            System.out.printf("%6.4f ", time);
        System.out.println();




    }
}
