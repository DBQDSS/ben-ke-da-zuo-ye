package task2;

public class Test {
    public static void main(String[] args) {
        // 创建一个字符串类型的 LeakyStack
        LeakyStack<String> stringStack = new LeakyStack<>(3);
        stringStack.push("Hello");
        stringStack.push("World");
        stringStack.push("!");
        System.out.print("目前栈中元素为：");
        stringStack.showStack();

        System.out.println("顶端元素: " + stringStack.peek());
        // 应该显示 "!" 75. 76. // 入栈新元素，这将导致最早的元素被移除
        stringStack.push("Java");
        System.out.print("压入'Java'之后: " );
        stringStack.showStack();
        System.out.println();
        // 应该移除并返回 "World" 81. 82. System.out.println();

        // 创建一个整数类型的 LeakyStack
        LeakyStack<Integer> integerStack = new LeakyStack<>(5);
        integerStack.push(1);
        integerStack.push(2);
        integerStack.push(3);
        integerStack.push(4);
        integerStack.push(5);
        System.out.println("原始数据:");
        integerStack.showStack();
        integerStack.push(6);
        System.out.println("操作之后:");
        integerStack.showStack();
        System.out.println();

        // 创建一个整数类型的 LeakyStack
        LeakyStack<Character> charStack = new LeakyStack<>(5);
        charStack.push('a');
        charStack.push('b');
        charStack.push('c');
        charStack.push('d');
        charStack.push('e');
        System.out.println("原始数据:");
        charStack.showStack();
        charStack.push('f');
        System.out.println("操作之后:");
        charStack.showStack();
    }
}
