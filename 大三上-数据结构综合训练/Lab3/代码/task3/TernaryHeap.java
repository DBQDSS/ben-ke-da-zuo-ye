package task3;

public class TernaryHeap extends MinHeap {
    public TernaryHeap(int capacity) {
        super(capacity);
    }

    @Override
    protected void heapifyUp(int index) {
        int parentIdx = (index - 1) / 3;
        if (index > 0 && heap[parentIdx] > heap[index]) {
            swap(parentIdx, index);
            heapifyUp(parentIdx);
        }
    }

    @Override
    protected void heapifyDown(int index) {
        int smallest = index;
        int childIndex1 = 3 * index + 1;
        int childIndex2 = 3 * index + 2;
        int childIndex3 = 3 * index + 3;

        if (childIndex1 < size && heap[childIndex1] < heap[smallest]) {
            smallest = childIndex1;
        }
        if (childIndex2 < size && heap[childIndex2] < heap[smallest]) {
            smallest = childIndex2;
        }
        if (childIndex3 < size && heap[childIndex3] < heap[smallest]) {
            smallest = childIndex3;
        }

        if (smallest != index) {
            swap(index, smallest);
            heapifyDown(smallest);
        }
    }
}
