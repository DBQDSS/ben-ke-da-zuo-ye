package task2;

import java.util.Random;

public class GenerateData {

    //生成重复的序列
    //用 0 <= proportion <= 1 表示重复率
    //随机重复
    public static Double[] getRandomRepeat(int N,double proportion){
        Double[] numbers=getSortedData(N);
        for(int i = 0;i < N * proportion; i++){
            numbers[i] = -1.0;
        }
        shuffle(numbers,0, numbers.length);
        return numbers;
    }

    //正序重复
    public static Double[] getSortedRepeat(int N,double proportion){
        Double[] numbers = getSortedData(N);
        for(int i = 0; i < N * proportion; i++){
            numbers[i] = -1.0;
        }
        return numbers;
    }

    //逆序重复
    public static Double[] getInversedRepeat(int N,double proportion){
        Double[] numbers = getInversedData(N);
        for(int i = (int) (N * proportion); i < N; i++){
            numbers[i] = 9999.0;
        }
        return numbers;
    }


    //生成问题5所要求的数据序列
    public  static  Double[] getSortedSome(int N){
        int node1=N/2;
        int node2=N/4+node1;
        int node3=N/8+node2;
        Double[] numbers=new Double[N];
        for(int i=0;i<node1;i++){
            numbers[i]=0.0;
        }
        for(int i=node1;i<node2;i++){
            numbers[i]=1.0;
        }
        for(int i=node2;i<node3;i++){
            numbers[i]=2.0;
        }
        for(int i=node3;i<N;i++){
            numbers[i]=3.0;
        }
        return numbers;
    }
    public static  Double[] getRandomSome(int N) {
        Double[] numbers = getSortedSome(N);
        shuffle(numbers, 0, numbers.length);
        return numbers;
    }
    public  static  Double[] getInversedSome(int N){
        int node1 = N / 8;
        int node2 = N / 8 + node1;
        int node3 = N / 4 + node2;
        Double[] numbers = new Double[N];
        for(int i = 0;i < node1; i++){
            numbers[i] = 3.0;
        }
        for(int i = node1; i < node2; i++){
            numbers[i] = 2.0;
        }
        for(int i=node2;i < node3;i++){
            numbers[i]=1.0;
        }
        for(int i=node3;i<N;i++){
            numbers[i]=0.0;
        }
        return numbers;
    }

    // 生成一个长度为N的均匀分布的数据序列
    public static Double[] getRandomData(int N){
        Double[] numbers = getSortedData(N);
        shuffle(numbers, 0, numbers.length);
        return numbers;
    }
    // 生成一个长度为N的正序的数据序列
    public static Double[] getSortedData(int N){
        Double[] numbers = new Double[N];
        double t = 0.0;
        for (int i = 0; i < N; i++){
            numbers[i] = t;
            t = t + 1.0/N;
        }
        return numbers;
    }
    // 生成一个长度为N的逆序的数据序列
    public static Double[] getInversedData(int N){
        Double[] numbers = new Double[N];
        double t = 1.0;
        for (int i = 0; i < N; i++){
            t = t - 1.0/N;
            numbers[i] = t;
        }
        return numbers;
    }

    // 将数组numbers中的[left,right)范围内的数据随机打乱
    private static void shuffle(Double[] numbers, int left, int right){
        int N = right - left;
        Random rand = new Random();
        for(int i = 0; i < N; i++){
            int j = i + rand.nextInt(N-i);
            exchange(numbers, i+left, j+left);
        }
    }

    private static void exchange(Double[] numbers, int i, int j){
        double temp = numbers[i];
        numbers[i] = numbers[j];
        numbers[j] = temp;
    }

    public static void main(String[] args) {
        Double[] numbers = getRandomData(1000);
        for(int i = 0; i < 100; i++)
            System.out.printf("%5.3f ", numbers[i]);
    }
}