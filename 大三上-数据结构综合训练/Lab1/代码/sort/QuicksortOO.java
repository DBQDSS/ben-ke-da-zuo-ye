package sort;

public class QuicksortOO extends QuicksortO{

    public QuicksortOO(int gap){
        super(gap);

    }
    @Override
    public void qsort(Comparable[] objs,int i,int j){
        if(j-i<3){
            insertsort(objs,i,j);
        }else{
            int pivoindex = findpivot(objs,i,j);

            int[] edge = findedge2Ways(objs,i,j,pivoindex);
            int leftedge = edge[0];
            int rightedge = edge[1];

            if((leftedge - i) > 1)
                qsort(objs,i,leftedge-1);
            if((j - rightedge) > 1)
                qsort(objs,rightedge+1,j);
        }
    }

    public int[] findedge2Ways(Comparable[] objs,int left,int right,int pivoindex){
        int lt = left;
        int gt = right;
        int index = left + 1;
        Comparable pivot = objs[pivoindex];
        exchange(objs,left,pivoindex);

        while (index <= gt) {
            int cmp = objs[index].compareTo(pivot);
            if (cmp < 0) {
                exchange(objs, lt++, index++);
            } else if (cmp > 0) {
                exchange(objs, index, gt--);
            } else {
                index++;
            }
        }


        return new int[]{lt, gt};

    }
}
