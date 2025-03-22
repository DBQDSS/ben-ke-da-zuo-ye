package task2;

public class LeakyStack <T>{
    private T[] stack;
    private int top;
    private int capacity;
    private int front;

    //构造函数
    public LeakyStack(int capacity){
        this.capacity = capacity;
        stack = (T[]) new Object[capacity];
        this.top = -1;
        this.front = -1;
    }
    public LeakyStack(){
        this(5);
    }


    //入栈
    public void push(T element){
        if ((top + 1) % capacity == front)
            front = (front + 1) % capacity;

        top = (top + 1) % capacity;
        stack[top] = element;

        if (front == -1)
            front++;
    }

    //出栈
    public T pop(){
        if(top == -1){
            System.out.println("Stack is Empty");
            return null;
        }
        T temp = stack[top];
        top = (top - 1 + capacity) % capacity;
        return temp;
    }

    // 查看栈顶元素
    public T peek() {
        if (top == -1) {
            throw new IllegalStateException("Stack is empty");
        }

        return stack[top];
    }

    //判断栈空
    public boolean isEmpty(){
        return top == -1;
    }

    //判断栈满
    public boolean isFull(){
        return (top + 1) % capacity == 0;
    }

    //显示栈内元素
    public void showStack(){
        if (front > top) {
            for (int i = front; i < capacity; i++)
                System.out.print(stack[i] + " ");
            for(int i = 0; i <= top; i++){
                System.out.print(stack[i]+ " ");
            }
            System.out.println();
        } else {
            for (int i = front; i <= top; i++)
                System.out.print(stack[i] + " ");
            System.out.println();
        }
    }

}

