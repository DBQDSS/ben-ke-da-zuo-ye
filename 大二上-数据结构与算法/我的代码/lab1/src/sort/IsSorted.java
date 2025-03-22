package sort;

import static java.util.Arrays.sort;

public class IsSorted {

    public static void main(String[] args){
        SortAlgorithm[] algs = new SortAlgorithm[]{new Quicksort(),new QuicksortO(7),new QuicksortOO(7)};
        Double[] arr=GenerateData.getRandomData(1000);

        //分别输出三种排序的结果
        //插入排序
        algs[0].sort(arr);
        System.out.println("未优化的快速排序的测试结果为:" + algs[0].isSorted(arr));
        //选择排序：
        algs[1].sort(arr);
        System.out.println("一次优化快速排序的测试结果为:" + algs[1].isSorted(arr));
        //希尔排序：
        algs[2].sort(arr);
        System.out.println("三路划分快速排序的测试结果为:" + algs[2].isSorted(arr));
    }

}

