package task3;

public class MinHeap extends Heap {

    public MinHeap(int capacity) {
        super(capacity);
    }

    @Override
    protected void heapifyUp(int index) {
        int parentIdx = (index - 1) / 2;
        if (index > 0 && heap[parentIdx] > heap[index]) {
            swap(parentIdx, index);
            heapifyUp(parentIdx);
        }
    }

    @Override
    protected void heapifyDown(int index) {
        int smallest = index;
        int leftChildIdx = 2 * index + 1;
        int rightChildIdx = 2 * index + 2;

        if (leftChildIdx < size && heap[leftChildIdx] < heap[smallest]) {
            smallest = leftChildIdx;
        }
        if (rightChildIdx < size && heap[rightChildIdx] < heap[smallest]) {
            smallest = rightChildIdx;
        }
        if (smallest != index) {
            swap(index, smallest);
            heapifyDown(smallest);
        }
    }
}
