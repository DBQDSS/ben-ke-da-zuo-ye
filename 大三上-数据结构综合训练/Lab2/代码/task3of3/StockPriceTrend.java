package task3of3;
import java.util.Stack;

public class StockPriceTrend {
    public static int[] calculateSpanNaive(int[] prices) {
        int n = prices.length;
        int[] s = new int[n];

        for (int i = 0; i < n; i++) {
            int span = 1;
            for (int j = i - 1; j >= 0 && prices[j] <= prices[i]; j--) {
                span++;
            }
            s[i] = span;
        }
        return s;
    }

    public static int[] calculateSpanWithStack(int[] prices) {
        int n = prices.length;
        int[] s = new int[n];
        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && prices[stack.peek()] <= prices[i]) {
                stack.pop();
            }
            s[i] = (stack.isEmpty()) ? (i + 1) : (i - stack.peek());
            stack.push(i);
        }
        return s;
    }

    public static void main(String[] args) {
        int[] prices = {100, 80, 60, 70, 60, 75, 85};
        int[] result2 = calculateSpanNaive(prices);
        int[] result1 = calculateSpanWithStack(prices);
        System.out.print("朴素方法：");
        for (int span : result1) {
            System.out.print(span + " ");
        }
        System.out.println();
        System.out.print("栈方法：");
        for (int span : result2) {
            System.out.print(span + " ");
        }
    }
}

