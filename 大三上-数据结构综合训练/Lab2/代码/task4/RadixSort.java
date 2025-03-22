package task4;

import java.io.*;
import java.util.Scanner;

public class RadixSort {

    public static void radixSortForInteger(int[] arr) {
        int max = Integer.MIN_VALUE;
        for (int value : arr) {
            if (value >= max) {
                max = value;
            }
        }
        int maxlength = Integer.toString(max).length();

        Queue<Integer>[] buckets = new Queue[10];
        for(int i = 0; i < buckets.length; i++)
            buckets[i] = new Queue<Integer>();

        for (int i = 0, n = 1; i < maxlength; i++, n = n * 10) {
            for (int value : arr) {
                int num = (value / n) % 10;
                buckets[num].enqueue(value);
            }
            int index = 0;
            for (Queue queue : buckets) {
                while (!queue.isEmpty()) {
                    arr[index] = (int) queue.dequeue();
                    index++;
                }
            }
        }

    }

    public static void writeToFile1(int[] array, String filePath) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            int index=0;
            for (int value : array) {
                writer.write(value +"  ");
                index++;
                if(index==10){
                    writer.write("\n");
                    index=0;
                }
            }
        }
    }

    public static void writeToFile2(String[] array, String filePath) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            int index=0;
            for (String value : array) {
                writer.write(value +"  ");
                index++;
                if(index==10){
                    writer.write("\n");
                    index=0;
                }
            }
        }
    }

    public static void radixSortForString(String[] strings ){
        int maxlength=strings[0].length();

        Queue[] temp = new Queue[52];
        for(int i = 0; i < temp.length; i++)
            temp[i] = new Queue<String>();

        for (int i = 0; i < maxlength; i++) {
            for (String string : strings) {
                char c = string.charAt(maxlength - 1 - i);
                int num = c >= 'a' ? c - 'a' + 26 : c - 'A';
                temp[num].enqueue(string);
            }
            int index = 0;
            for (Queue queue : temp) {
                while (!queue.isEmpty()) {
                    strings[index] = (String) queue.dequeue();
                    index++;
                }
            }
        }

    }

    public static boolean isSortedOfNums(int[] nums){
        for(int i=0;i< nums.length-1;i++){
            if(nums[i]>nums[i+1]){
                return false;
            }
        }
        return true;
    }
    public static boolean isSortedOfStrings(String[] strings){
        for(int i=0;i< strings.length-1;i++){
            if(strings[i].compareTo(strings[i+1])>0){
                return false;
            }
        }
        return true;
    }

    public static String[] getStrings(String filename) throws FileNotFoundException {
        Scanner in= new Scanner(new File(filename));
        StringBuffer sb=new StringBuffer();
        String temp=in.next();
        sb.append(temp);
        temp=in.next();
        while(!temp.equals("stop")){
            sb.append('\n');
            sb.append(temp);
            temp=in.next();
        }
        return sb.toString().split("\n");
    }


    public static int[] getNums(String filename) throws FileNotFoundException {
        Scanner in=new Scanner(new File(filename));
        StringBuffer sb=new StringBuffer();
        String temp=in.next();
        sb.append(temp);
        temp=in.next();
        while(!temp.equals("stop")){
            sb.append('\n');
            sb.append(temp);
            temp=in.next();
        }
        int[] nums= new int[sb.toString().split("\n").length];
        for(int i = 0; i < nums.length; i++){
            nums[i]=Integer.parseInt(sb.toString().split("\n")[i]);
        }
        return  nums;
    }

}
