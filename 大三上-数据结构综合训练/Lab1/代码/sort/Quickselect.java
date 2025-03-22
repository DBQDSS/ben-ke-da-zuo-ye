package sort;

public class Quickselect extends Quicksort{
    public Comparable selectK(Comparable[] objs, int k){
        if(k < 1 || k > objs.length){
            throw new IllegalArgumentException("OUT OF THE SCOPE");
        } else{
            return select(objs, k, 0, objs.length-1);
        }
    }
    public Comparable select(Comparable[] objs, int k, int i, int j){
        int pivoindex = findpivot(objs, i, j);
        exchange(objs, pivoindex, j);
        int p = partition(objs, i - 1, j, objs[j]);
        exchange(objs, p, j);
        if(p == k)
            return objs[p];
        return p < k ? select(objs, k, p + 1, j) : select(objs, k, i, p - 1);
    }

    public Comparable selectKDerect(Comparable[] objs,int k){
        if( k < 1 || k > objs.length){
            throw new IllegalArgumentException("OUT OF THE SCOPE");
        } else{
            return selectDerect(objs,k,0, objs.length-1);
        }
    }

    public Comparable selectDerect(Comparable[] objs,int k,int i,int j){
        sort(objs);
        return objs[k];
    }
}

