package task3;

public abstract class Heap {
    protected int[] heap;
    protected int size;
    protected int capacity;

    public Heap(int capacity) {
        this.capacity = capacity;
        this.heap = new int[capacity];
        this.size = 0;
    }

    protected abstract void heapifyUp(int index);
    protected abstract void heapifyDown(int index);

    protected void swap(int i, int j) {
        int temp = heap[i];
        heap[i] = heap[j];
        heap[j] = temp;
    }

    public void insert(int element) {
        if (size >= capacity) {
            throw new IllegalStateException("Heap is full");
        }
        heap[size] = element;
        heapifyUp(size);
        size++;
    }

    public int delete() {
        if (size == 0) {
            throw new IllegalStateException("Heap is empty");
        }
        int minElement = heap[0];
        heap[0] = heap[size - 1];
        size--;
        heapifyDown(0);
        return minElement;
    }

    public int getSize() {
        return size;
    }

    public int getMin() {
        if (size == 0) {
            throw new IllegalStateException("Heap is empty");
        }
        return heap[0];
    }

    public class HeapSort {

        public static void sort(Heap heap, int[] array) {
            for (int i = 0; i < array.length; i++) {
                heap.insert(array[i]);
            }
            for (int i = 0; i < array.length; i++) {
                array[i] = heap.delete();
            }
        }
    }

}
