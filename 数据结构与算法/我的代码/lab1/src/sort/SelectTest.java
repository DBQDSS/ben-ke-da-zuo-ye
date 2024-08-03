package sort;

import static java.util.Arrays.sort;

public class SelectTest extends SortTest{


    public static double timeQuick(Quickselect sel, Double[] numbers,int K){
        double start = System.nanoTime();
        sel.selectK(numbers,K);
        double end = System.nanoTime();
        return end - start;
    }
    public static double timeDerect(Quickselect sel, Double[] numbers,int K){
        double start = System.nanoTime();
        sel.selectKDerect(numbers,K);
        double end = System.nanoTime();
        return end - start;
    }

    public static double[] testQuick(Quickselect sel, int length, int T)
    {
        Double[][] numbers =new Double[][]{GenerateData.getRandomData(length),GenerateData.getSortedData(length),
                GenerateData.getInversedData(length),GenerateData.getSortedSome(length)};

        double[] totalTime = new double[numbers.length];
        for(int j=0;j< numbers.length;j++){
            for(int i = 0; i < T; i++){
                totalTime[j] += timeQuick(sel, numbers[j], numbers.length/2);}
            totalTime[j]/=T;
        }
        return totalTime;
    }
    public static double[] testDerect(Quickselect sel, int length, int T)
    {
        Double[][] numbers =new Double[][]{GenerateData.getRandomData(length),GenerateData.getSortedData(length),
                GenerateData.getInversedData(length),GenerateData.getRandomSome(length)};

        double[] totalTime = new double[numbers.length];
        for(int j=0;j< numbers.length;j++){
            for(int i = 0; i < T; i++){
                totalTime[j] += timeDerect(sel, numbers[j], numbers.length/2);}
            totalTime[j]/=T;
        }
        return totalTime;
    }


    public static void main(String[] args) {

        System.out.println("以下每行分别是数据量在100, 1000, 10000, 100000时程序运行的时间开销");
        System.out.println();

        //数据量
        int[] dataLength = {100, 1000, 10000, 100000};
        double[][] elapsedTime = new double[dataLength.length][];
        String[] arr = {"随机数据", "正序数据", "逆序数据", "重复数据"};
        Quickselect quickselect = new Quickselect();
        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = testQuick(quickselect, dataLength[i], 100);
        System.out.println("快速选择法的时间开销：");
        for(double time[]: elapsedTime) {
            for (int k = 0; k < time.length; k++) {
                System.out.print(arr[k] + " ");
                System.out.printf("%6.4f ", time[k]);
            }
            System.out.println();
        }
        System.out.println();

        System.out.println("暴力查找法的时间开销");
        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = testDerect(quickselect, dataLength[i], 100);
        for(double time[]: elapsedTime) {
            for (int k = 0; k < time.length; k++) {
                System.out.print(arr[k] + " ");
                System.out.printf("%6.4f ", time[k]);
            }
            System.out.println();
        }

        /*
        System.out.println("验证快速选择算法的正确性");
        Integer[] array = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
        Quickselect quicksel = new Quickselect();

        // Test QuickSelect
        Comparable resultQuickSelect = quicksel.selectK(array, 5);
        System.out.println("QuickSelect Result: " + resultQuickSelect);

        // Test Direct Sorting
        Comparable resultDirectSort = quicksel.selectKDerect(array, 5);
        System.out.println("Direct Sorting Result: " + resultDirectSort);

        int[] dataLength = {100, 1000, 10000, 100000};
        double[][] elapsedTime = new double[dataLength.length][];
        Quickselect quickselect = new Quickselect();
        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = testQuick(quickselect, dataLength[i], 5);
        System.out.println("不同数据量下使用快速查找法，随机数据，正序数据，逆序数据以及重复数据的查找时间:");
        for(double time[]: elapsedTime) {
            for (int k = 0; k < time.length; k++) {
                System.out.printf("%6.4f ", time[k]);
            }
            System.out.println();
        }
        System.out.println();


        System.out.println("不同数据量下在随机数据，正序数据，逆序数据以及重复数据的查找时间：");
        for(int i = 0; i < dataLength.length; i++)
            elapsedTime[i] = testDerect(quickselect, dataLength[i], 5);
        for(double time[]: elapsedTime) {
            for (int k = 0; k < time.length; k++) {
                System.out.printf("%6.4f ", time[k]);
            }
            System.out.println();
        }
        System.out.println();
        */
    }
}
