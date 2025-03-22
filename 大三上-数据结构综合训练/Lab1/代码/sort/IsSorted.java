package sort;

public class IsSorted {

    public static void main(String[] args){
        SortAlgorithm[] algs = new SortAlgorithm[]{new Insertion(), new Selection(),
                new Quicksort(), new Mergesort(), new Shell(), new Shell2(), new Shell3()};
        Double[] arr=GenerateData.getRandomData(1000);

        //分别输出三种排序的结果
        //插入排序
        algs[0].sort(arr);
        System.out.println("插入排序的测试结果为:" + algs[0].isSorted(arr));
        //选择排序：
        algs[1].sort(arr);
        System.out.println("选择排序的测试结果为:" + algs[1].isSorted(arr));
        //快速排序：
        algs[2].sort(arr);
        System.out.println("快速排序的测试结果为:" + algs[2].isSorted(arr));
        //归并排序：
        algs[3].sort(arr);
        System.out.println("归并排序的测试结果为:" + algs[3].isSorted(arr));
        //Shell策略：
        algs[4].sort(arr);
        System.out.println("Shell间隔策略的希尔排序测试结果为:" + algs[4].isSorted(arr));
        //Hibbard策略：
        algs[5].sort(arr);
        System.out.println("Hibbard间隔策略的希尔排序测试结果为:" + algs[5].isSorted(arr));
        //Knuth策略：
        algs[6].sort(arr);
        System.out.println("Knuth间隔策略的希尔排序测试结果为:" + algs[6].isSorted(arr));
    }

}

