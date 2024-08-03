package task3;

import java.util.Random;

public class GenerateData {
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
