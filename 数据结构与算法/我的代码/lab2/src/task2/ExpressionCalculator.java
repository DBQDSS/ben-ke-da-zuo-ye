package task2;

import java.util.Stack;

public class ExpressionCalculator {
    public static double calculator(String expression){
        Stack<Double> number = new Stack<>();
        Stack<Character> operator = new Stack<>();
        for(int i=0;i<expression.length();i++){
            char c=expression.charAt(i);
            //�����ո�
            if(c==' '){
                continue;
            }

            //���ִ���
            if(c>='0'&&c<='9'||c=='.'){
                StringBuffer sb=new StringBuffer();
                while(i<expression.length()&&
                        (expression.charAt(i)>'0'
                                &&expression.charAt(i)<'9'
                                ||expression.charAt(i)=='.')){

                    sb.append(expression.charAt(i++));

                }
                i--;
                number.push(Double.parseDouble(sb.toString()));
            }

            //���Ŵ���

            //���Ŵ���
            else if (c=='(') {
                operator.push(c);
            }
            else if(c==')'){
                while(operator.peek()!='('){
                    number.push(applyOp(operator.pop(),number.pop(),number.pop()));
                }
                operator.pop();
            }

            //���������
            else if (c=='+'||c=='-'||c=='*'||c=='/'||c=='^') {
                while(!operator.isEmpty()&& hasPrecedence(c,operator.peek())){
                    number.push(applyOp(operator.pop(),number.pop(),number.pop()));
                }
                operator.push(c);
            }
        }
        while(!operator.isEmpty()){
            number.push((applyOp(operator.pop(),number.pop(),number.pop())));
        }
        return number.pop();
    }

    private static boolean hasPrecedence(char c, Character peek) {
        if(peek=='('||peek==')'){
            return false;
        }
        if((c=='*'||c=='/')&&(peek=='+'||peek=='-')){
            return false;
        }
        if((c=='^')&&(peek=='+'||peek=='-'||peek=='*'||peek=='/')){
            return false;
        }
        return true;
    }

    private static double applyOp(char op,double num2,double num1){
        switch (op){
            case '+': return num1+num2;
            case '-':return num1-num2;
            case '*':return num1*num2;
            case '/':return num1/num2;
            case '^':return Math.pow(num1,num2);
        }
        return 0;
    }


    public static void main(String[] args){
        String expression="2 + 5 * 6- (6 /3  )^2 ";
        System.out.println("The result of   "+expression+"=   "+calculator(expression));
    }
}

