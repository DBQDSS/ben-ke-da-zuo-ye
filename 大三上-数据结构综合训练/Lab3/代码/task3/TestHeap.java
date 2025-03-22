package task3;

public class TestHeap {
    public static void main(String[] args) {
        testHeap(new MinHeap(10), "BinaryHeap");
        testHeap(new TernaryHeap(10), "TernaryHeap");
    }

    private static void testHeap(Heap heap, String heapType) {
        System.out.println("Testing " + heapType);

        heap.insert(22);
        heap.insert(1);
        heap.insert(6);
        heap.insert(20);
        heap.insert(24);
        heap.insert(9);

        System.out.println("Min element: " + heap.getMin());

        System.out.println("Deleting elements:");
        while (heap.getSize() > 0) {
            System.out.print(heap.delete() + " ");
        }
        System.out.println();

        int[] array = {25, 3, 13, 8, 6, 2};
        Heap.HeapSort.sort(heap, array);
        System.out.println("Sorted array:");
        for (int value : array) {
            System.out.print(value + " ");
        }
        System.out.println();

        try {
            heap.delete();
        } catch (IllegalStateException e) {
            System.out.println("Caught exception on delete from empty heap: " + e.getMessage());
        }

        try {
            for (int i = 0; i < 11; i++) {
                heap.insert(i);
            }
        } catch (IllegalStateException e) {
            System.out.println("Caught exception on insert into full heap: " + e.getMessage());
        }

        System.out.println("Testing " + heapType + " completed.\n");
    }
}
