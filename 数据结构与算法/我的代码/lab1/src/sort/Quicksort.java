package sort;

public class Quicksort extends SortAlgorithm {
    public int gap;

    public void sort(Comparable[] objs) {
        qsort(objs, 0, objs.length - 1);
    }

    public void qsort(Comparable[] objs, int i, int j) {
        int pivoindex = findpivot(objs, i, j);
        exchange(objs, pivoindex, j);
        int k = partition(objs, i - 1, j, objs[j]);
        exchange(objs, k, j);
        if ((k - i) > 1) qsort(objs, i, k - 1);
        if ((j - k) > 1) qsort(objs, k + 1, j);
    }


    public int findpivot(Comparable[] objs, int i, int j) {
        if (less(objs[i], objs[j]) && less(objs[(i + j) / 2], objs[i])) {
            return i;
        } else if (less(objs[j], objs[i]) && less(objs[(i + j) / 2], objs[j])) {
            return j;
        } else {
            return (i + j) / 2;
        }
    }


    public int partition(Comparable[] objs, int i, int j, Comparable pivot) {

        do {
            while (less(objs[++i], pivot)) ;
            while ((j != 0) && (less(pivot, objs[--j]))) ;
            exchange(objs, i, j);
        } while (i < j);

        exchange(objs, i, j);
        return i;
    }
}

