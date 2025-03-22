package task1and2;

class Node<T> {
    T data;
    Node<T> next;
    Node<T> prev;

    Node(T data) {
        this.data = data;
    }
}

public class LinkedListDQueue<T> implements DQueue<T> {
    private Node<T> front, rear;
    private int size;

    public LinkedListDQueue() {
        front = rear = null;
        size = 0;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public boolean isFull() {
        return false; // 链表实现不可能满
    }

    public int size() {
        return size;
    }

    public void enqueueToRear(T element) throws ListException {
        if (element == null) throw new ListException("Element cannot be null");
        Node<T> newNode = new Node<>(element);
        if (isEmpty()) {
            front = rear = newNode;
        } else {
            rear.next = newNode;
            newNode.prev = rear;
            rear = newNode;
        }
        size++;
    }

    public void enqueueToFront(T element) throws ListException {
        if (element == null) throw new ListException("Element cannot be null");
        Node<T> newNode = new Node<>(element);
        if (isEmpty()) {
            front = rear = newNode;
        } else {
            newNode.next = front;
            front.prev = newNode;
            front = newNode;
        }
        size++;
    }

    public T dequeueFromFront() {
        if (isEmpty()) return null;
        T result = front.data;
        front = front.next;
        if (front != null) front.prev = null;
        else rear = null; // Reset rear if empty
        size--;
        return result;
    }

    public T dequeueFromRear() {
        if (isEmpty()) return null;
        T result = rear.data;
        rear = rear.prev;
        if (rear != null) rear.next = null;
        else front = null; // Reset front if empty
        size--;
        return result;
    }

    public T getFront() {
        return isEmpty() ? null : front.data;
    }

    public T getRear() {
        return isEmpty() ? null : rear.data;
    }
}