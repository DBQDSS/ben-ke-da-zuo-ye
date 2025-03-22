package task4;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;

import static task4.RadixSort.*;

public class Test {
    public static void main(String[] rags) throws IOException {
        int[] nums = getNums("D:\\MyJavaProject\\hw3\\src\\task4\\radixsort1.txt");
        String[] strings = getStrings("D:\\MyJavaProject\\hw3\\src\\task4\\radixsort2.txt");
        radixSortForInteger(nums);
        writeToFile1(nums, "D:\\MyJavaProject\\hw3\\src\\task4\\outputIntegers.txt");
        System.out.println(isSortedOfNums(nums) ?
                "the numbers have been sorted!" : "the numbers are not sorted!");
        radixSortForString(strings);
        writeToFile2(strings, "D:\\MyJavaProject\\hw3\\src\\task4\\outputStrings.txt");
        System.out.println(isSortedOfStrings(strings) ?
                "the strings have been sorted!" : "the strings are not sorted!");
    }

}
