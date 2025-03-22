package sort;

public class Mergesort extends SortAlgorithm{

    @Override
    public void sort(Comparable[] objs) {
        Comparable[] temp=new Comparable[objs.length];
        mergesort(objs,0,objs.length-1,temp);
    }

    public void mergesort(Comparable[] objs,int low,int high,Comparable[] temp){
        if(low>=high){return;}
        int mid=low+(high-low)/2;
        mergesort(objs, low, mid, temp);
        mergesort(objs, mid+1, high, temp);
        merge(objs,low,mid,high,temp);
    }

    public void merge(Comparable[] objs, int low, int mid, int high, Comparable[] temp){
        for(int i=low;i<=high;i++){
            temp[i]=objs[i];
        }
        int i=low;
        int j=mid+1;
        for(int p=low;p<=high;p++){
            if(i==mid+1){
                objs[p]=temp[j++];
            } else if (j>high) {
                objs[p]=temp[i++];
            }else if(less(temp[j],temp[i] )){
                objs[p]=temp[j++];
            }else {
                objs[p]=temp[i++];
            }
        }
    }

}
