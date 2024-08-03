package task1;

public class Node<E> {
    E data;
    Node<E> next;

    Node(E data) {
        this.data = data;
        next = null;
    }
}