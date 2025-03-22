package task1and2;

public class DLink<T> {
    private T element;
    private DLink next;
    private DLink prev;

    public DLink() {
        this(null, null);
    }

    public DLink(DLink prevVal, DLink nextVal) {
        this(null, prevVal, nextVal);
    }

    public DLink(T element, DLink prevVal, DLink nextVal) {
        this.element = element;
        next = nextVal;
        prev = prevVal;
    }

    public DLink next() {
        return next;
    }

    public DLink setNext(DLink next) {
        this.next = next;
        return this.next;
    }

    public DLink prev() {
        return prev;
    }

    public DLink setPrev(DLink prev) {
        this.prev = prev;
        return this.prev;
    }

    public T element() {
        return element;
    }

    public T setElement(T element) {
        this.element = element;
        return this.element;
    }
}