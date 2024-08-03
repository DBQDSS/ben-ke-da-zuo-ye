package task3;

public class Queue <T>{
    Node head,tail;
    public Queue() {
        this.head = this.tail = null;
    }

    public boolean isEmpty() {
        return head == null;
    }

    public void enqueue(T value){
        Node temp = new Node<>(value);
        if(this.tail == null){
            this.head = this.tail = temp;
            return;
        }
        this.tail.next = temp;
        this.tail = temp;
    }


    public T dequeue(){
        if(isEmpty()){
            System.out.println("This Queue is Empty");
            return null;
        }
        T temp= (T) head.value;
        this.head = this.head.next;
        if(head == null){
            this.tail = null;
        }
        return  temp;
    }
}

