package task1and2;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class MaxInSlidingWindow {
    public static List<Integer> maxSlidingWindow(int[] nums, int k) {
        List<Integer> result = new ArrayList<>();
        DQueue<Integer> deque = new LinkedListDQueue<>();

        for (int i = 0; i < nums.length; i++) {
            // 移除不在当前窗口中的元素
            while (!deque.isEmpty() && deque.getFront() < i - k + 1) {
                deque.dequeueFromFront();
            }
            // 移除所有小于当前元素的元素
            while (!deque.isEmpty() && nums[deque.getRear()] < nums[i]) {
                deque.dequeueFromRear();
            }
            // 在双端队列的尾部添加当前元素的索引
            try {
                deque.enqueueToRear(i);
            } catch (ListException e) {
                e.printStackTrace(); // 处理异常
            }
            // 当第一个窗口完成时，添加最大值到结果中
            if (i >= k - 1) {
                result.add(nums[deque.getFront()]);
            }
        }

        return result;
    }

    public static void main(String[] args) {
        Random random = new Random();
        int numTests = 10; // 生成10组测试数据
        int arraySize = 10; // 每组数据的大小

        for (int test = 0; test < numTests; test++) {
            // 随机生成一组数据
            int[] data = new int[arraySize];
            for (int i = 0; i < arraySize; i++) {
                data[i] = random.nextInt(100); // 随机生成0到99之间的整数
            }
            int k = random.nextInt(arraySize) + 1; // 随机生成1到arraySize之间的k值

            // 打印生成的数据和k值
            System.out.println("测试数据: " + java.util.Arrays.toString(data) + ", k = " + k);

            // 计算每个窗口的最大值
            List<Integer> maxValues = maxSlidingWindow(data, k);
            System.out.println("滑动窗口最大值: " + maxValues);
            System.out.println(); // 添加空行以便于输出阅读
        }
    }
}