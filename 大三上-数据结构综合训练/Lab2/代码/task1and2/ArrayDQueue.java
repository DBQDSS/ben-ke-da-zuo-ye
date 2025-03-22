package task1and2;

public class ArrayDQueue<T> implements DQueue<T> {
    private T[] elements;
    private int front, rear, size, capacity;

    @SuppressWarnings("unchecked")
    public ArrayDQueue(int capacity) {
        this.capacity = capacity;
        this.elements = (T[]) new Object[capacity];
        this.front = -1;
        this.rear = 0;
        this.size = 0;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean isFull() {
        return size == capacity;
    }

    public int size() {
        return size;
    }

    public void enqueueToRear(T element) throws ListException {
        if (isFull()) throw new ListException("Queue is full");
        rear = (rear + 1) % capacity;
        elements[rear] = element;
        if (front == -1) front = rear; // First element added
        size++;
    }

    public void enqueueToFront(T element) throws ListException {
        if (isFull()) throw new ListException("Queue is full");
        front = (front - 1 + capacity) % capacity;
        elements[front] = element;
        if (rear == -1) rear = front; // First element added
        size++;
    }

    public T dequeueFromFront() {
        if (isEmpty()) return null;
        T result = elements[front];
        front = (front + 1) % capacity;
        size--;
        if (size == 0) front = -1; // Reset if empty
        return result;
    }

    public T dequeueFromRear() {
        if (isEmpty()) return null;
        T result = elements[rear];
        rear = (rear - 1 + capacity) % capacity;
        size--;
        if (size == 0) rear = -1; // Reset if empty
        return result;
    }

    public T getFront() {
        return isEmpty() ? null : elements[front];
    }

    public T getRear() {
        return isEmpty() ? null : elements[rear];
    }
}