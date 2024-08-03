package sort;

public class QuicksortO extends Quicksort{

    //优化快速排序算法的阀值
    public QuicksortO(int gap){
        this.gap = gap;
    }

    public void qsort(Comparable[] objs, int i, int j){
        if(j - i < 3){
            insertsort(objs,i,j);
        }else {
            int pivoindex = findpivot(objs,i,j);
            exchange(objs,pivoindex,j);
            int k = partition(objs,i-1,j,objs[j]);
            exchange(objs,k,j);
            if((k - i) > 1)qsort(objs,i,k-1);
            if((j - k) > 1)qsort(objs,k+1,j);}
    }


    public void insertsort(Comparable[] objs,int low,int high){
        for(int i = low + 1; i <= high; i++){
            for(int j = i; j > low && less(objs[j], objs[j-1]); j--){
                exchange(objs, j, j-1);
            }
        }
    }


}
