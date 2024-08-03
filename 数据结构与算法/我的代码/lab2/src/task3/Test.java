package task3;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;

import static task3.RadixSort.*;

public class Test {

    //文件地址
    public static void main(String[] rags) throws IOException {
        int[] nums = getNums("C:\\Users\\17519\\Desktop\\数据结构与算法\\李垚辰\\Lab2\\radixSort1.txt");
        String[] strings = getStrings("C:\\Users\\17519\\Desktop\\数据结构与算法\\李垚辰\\Lab2\\radixSort2.txt");
        radixSortForInteger(nums);
        writeToFile1(nums, "C:\\Users\\17519\\Desktop\\outputIntegers.txt");
        System.out.println(isSortedOfNums(nums) ?
                "The numbers have been sorted!" : "The numbers are not sorted!");
        radixSortForString(strings);
        writeToFile2(strings, "C:\\Users\\17519\\Desktop\\outputStrings.txt");
        System.out.println(isSortedOfStrings(strings) ?
                "The strings have been sorted!" : "The strings are not sorted!");
    }
}
