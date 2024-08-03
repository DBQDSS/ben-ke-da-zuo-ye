package task1;

public class Link<T> {
    private T element;
    private Link next;

    public Link() {
        this(null, null);
    }

    public Link(Link nextVal) {
        this(null, nextVal);
    }

    public Link(T element, Link nextVal) {
        this.element = element;
        next = nextVal;
    }

    public Link next() {
        return next;
    }

    public Link setNext(Link next) {
        this.next = next;
        return this.next;
    }

    public T element() {
        return element;
    }

    public T setElement(T element) {
        this.element = element;
        return this.element;
    }
}
