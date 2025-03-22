package task3of2;

import java.util.Stack;

public class ExpressionCalculator {
    public static double calculator(String expression) {
        Stack<Double> number = new Stack<>();
        Stack<Character> operator = new Stack<>();
        for (int i = 0; i < expression.length(); i++) {
            char c = expression.charAt(i);
            if (c == ' ') {
                continue;
            }

            if (Character.isDigit(c) || c == '.') {
                StringBuilder sb = new StringBuilder();
                while (i < expression.length() && (Character.isDigit(expression.charAt(i)) || expression.charAt(i) == '.')) {
                    sb.append(expression.charAt(i++));
                }
                i--;
                number.push(Double.parseDouble(sb.toString()));
            } else if (c == '(') {
                operator.push(c);
            } else if (c == ')') {
                while (!operator.isEmpty() && operator.peek() != '(') {
                    number.push(applyOp(operator.pop(), number.pop(), number.pop()));
                }
                if (!operator.isEmpty()) {
                    operator.pop(); // Pop the '('
                }
            } else if ("+-*/^".indexOf(c) >= 0) {
                while (!operator.isEmpty() && hasPrecedence(c, operator.peek())) {
                    number.push(applyOp(operator.pop(), number.pop(), number.pop()));
                }
                operator.push(c);
            }
        }
        while (!operator.isEmpty()) {
            number.push(applyOp(operator.pop(), number.pop(), number.pop()));
        }
        return number.pop();
    }

    private static boolean hasPrecedence(char c, Character peek) {
        if (peek == '(' || peek == ')') {
            return false;
        }
        if ((c == '*' || c == '/') && (peek == '+' || peek == '-')) {
            return false;
        }
        return !(c == '^' && (peek == '+' || peek == '-' || peek == '*' || peek == '/'));
    }

    private static double applyOp(char op, double num2, double num1) {
        switch (op) {
            case '+':
                return num1 + num2;
            case '-':
                return num1 - num2;
            case '*':
                return num1 * num2;
            case '/':
                if (num2 == 0) throw new ArithmeticException("Cannot divide by zero");
                return num1 / num2;
            case '^':
                return Math.pow(num1, num2);
        }
        return 0;
    }

    public static void main(String[] args) {
        // 测试用例
        String[] testExpressions = {
                "3 + 5",
                "10 + 2 * 6",
                "100 * 2 + 12",
                "100 * (2 + 12)",
                "100 * (2 + 12) / 14",
                "2 + 5 * 6 - (6 / 3) ^ 2)",
                "(3+2) * (5-4)"
        };

        for (String expr : testExpressions) {
            try {
                System.out.println("The result of " + expr + " = " + calculator(expr));
            } catch (Exception e) {
                System.out.println("Error evaluating expression: " + expr + " - " + e.getMessage());
            }
        }
    }
}
