package sort;

public class Selection extends SortAlgorithm{

    public void sort(Comparable[] objs){
        for(int i=0;i<objs.length-1;i++){
            int index=i;
            for(int j=i+1;j<objs.length;j++){
                if(less(objs[j],objs[index])){
                    index=j;
                }
            }
            exchange(objs,i,index);
        }
    }


}
