package task3;

import java.util.Stack;

public class QuickSortOfRecursion extends SortAlgorithm {
    @Override
    public void sort(Comparable[] objs) {
        Stack<Range> stack=new Stack<>();
        stack.push(new Range(0, objs.length-1));

        while (!stack.isEmpty()) {
            Range range=stack.pop();
            if(range.low<range.high){
                int pivot=partition(objs, range.low,range.high);
                stack.push(new Range(range.low,pivot-1));
                stack.push(new Range(pivot+1,range.high));
            }
        }
    }
    //˫ָ�뷨����Ԫ�ؽ���
    private int partition(Comparable[] objs,int low,int high){
        Comparable pivot=objs[high];
        int i=low-1;
        for (int j=low;j<high;j++){
            if(less(objs[j],pivot)||equals(objs[j],pivot)){
                i++;
                exchange(objs,i,j);
            }
        }
        exchange(objs,i+1,high);
        return i+1;
    }



    static class Range{
        int low,high;
        public Range(int low,int high){
            this.high=high;
            this.low=low;
        }
    }
    // ���Դ���
    public static void main(String[] args) {
        QuickSortOfRecursion sorter = new QuickSortOfRecursion();
        Comparable[] arr = {10, 7, 8, 9, 1, 5};
        sorter.sort(arr);
        System.out.println("Sorted array: ");
        sorter.show(arr);
    }

}
