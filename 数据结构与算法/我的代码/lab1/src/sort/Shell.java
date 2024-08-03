package sort;

public class Shell extends SortAlgorithm {

    @Override
    public void sort(Comparable[] objs) {
        int N = objs.length;
        int h = 1;
        do {
            h = h * 3 + 1;
        } while (h < N);

        while (h >= 1) {
            for (int i = h; i < N; i++) {
                Comparable temp = objs[i];
                int j;

                for (j = i; j >= h && less(temp, objs[j - h]); j -= h) {
                    objs[j] = objs[j - h];
                }

                objs[j] = temp;
            }

            h = (h - 1) / 3;
        }
    }
}