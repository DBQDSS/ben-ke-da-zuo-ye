package task1and2;

import java.io.*;
import java.util.Scanner;

public class Test1 {
    public static String getKey(String str){
        return str.split(" ")[1];
    }
    public static String getValue(String str){
        return str.split("\"")[1];
    }
    public static void readLine(BST<String, String> bst, PrintWriter pw,File file) throws IOException {
        Scanner in = new Scanner(file);
        String value = new String();
        String temp = new String();
        while(!temp.equals("stop")){
            temp = in.nextLine();
            switch (temp.charAt(0)) {
                case '+' -> {
                    if (temp.split(" ")[2].equals(")")) {
                        bst.insert(getKey(temp), "");
                        break;
                    }
                    bst.insert(getKey(temp), getValue(temp));
                }
                case '-' -> {
                    if((value = bst.remove(getKey(temp))) == null) {
                        pw.println("remove unsuccess ---" + getKey(temp));
                        System.out.println("remove unsuccess ---" + getKey(temp));
                        break;
                    }
                    value = value.equals("") ? "" : " " + value;
                    pw.println("remove success ---" + getKey(temp) + value);
                    System.out.println("remove success ---" + getKey(temp) + value);
                }
                case '?' -> {
                    if((value = bst.search(getKey(temp))) == null) {
                        pw.println("search unsuccess ---" + getKey(temp));
                        System.out.println("search unsuccess ---" + getKey(temp));
                        break;
                    }
                    value = value.equals("") ? "" : " " + value;
                    pw.println("search success ---" + getKey(temp) + value);
                    System.out.println("search success ---" + getKey(temp) + value);
                }
                case '=' -> {
                    if(!bst.update(getKey(temp), getValue(temp))) {
                        pw.println("update unsuccess ---" + getKey(temp));
                        System.out.println("update unsuccess ---" + getKey(temp));
                        break;
                    }
                    value = getValue(temp);
                    pw.println("update success ---" + getKey(temp) + " " + value);
                    System.out.println("update success ---" + getKey(temp) + " " + value);
                }
                case '#' -> bst.showStructure(pw);
            }
        }
        in.close();
    }

    private static void compareFiles(String file1, String file2) throws IOException {
        BufferedReader br1 = new BufferedReader(new FileReader(file1));
        BufferedReader br2 = new BufferedReader(new FileReader(file2));

        String line1 = br1.readLine();
        String line2 = br2.readLine();

        boolean areEqual = true;
        int lineNum = 1;

        while (line1 != null || line2 != null) {
            if(line1 == null || line2 == null || !line1.equals(line2)) {
                areEqual = false;
                break;
            }
            line1 = br1.readLine();
            line2 = br2.readLine();
            lineNum++;
        }

        if (areEqual) {
            System.out.println("两个文件的内容相同。");
        } else {
            System.out.println("两个文件内容不同。它们在第 " + lineNum + " 行不同");
            System.out.println("File1 在第 " + lineNum + " 行的内容为 " +
                    line1 + "，File2 在第 " + lineNum + " 行的内容是 " + line2);
        }

        br1.close();
        br2.close();
    }

    public static void index(BST bst, PrintWriter pw, File file) throws IOException {
        Scanner in = new Scanner(file);
        String temp = in.nextLine();
        int line = 0;
        while(!temp.equals("stop")){
            for(String str : temp.split("[\n,.?!\";'()*\\-]|--|\\s+")) {
                if ("".equals(str) || str.length() < 3)
                    continue;
                bst.insert1(str, new StringBuilder(line + ""));
            }
            temp =in.nextLine();
            line++;
        }
        bst.printInorder(pw);
        in.close();
    }

    public static void main(String[] args) throws IOException {
        /*
        // 第一题
        String filename="task1and2\\BST_testcases.txt";
        // 保存 PrintWriter 输出的文件
        String outputFilename = "task1and2\\output.txt";
        // 待比较的结果文件
        String resultFilename = "task1and2\\BST_result.txt";

        BST<String,String> bst = new BST<String,String>();
        PrintWriter pw = new PrintWriter(new FileWriter(outputFilename));
        readLine(bst, pw,new File(filename));
        pw.close();
        // 比较两个文件的内容
        compareFiles(outputFilename, resultFilename);
        pw.close();
        */
        // 第二题
        String filename="task1and2\\BST_testcases.txt";
        String outputFilename = "task1and2\\output.txt";
        String resultFilename = "task1and2\\BST_result.txt";

        BST<String,String> bst = new BST<String,String>();
        PrintWriter pw = new PrintWriter(new FileWriter(outputFilename));
        readLine(bst, pw,new File(filename));

        pw.close();
        compareFiles(outputFilename, resultFilename);

        BST bstindex = new BST();
        File file = new File("task1and2\\article.txt");
        PrintWriter pwi = new PrintWriter("task1and2\\index_result.txt");

        index(bstindex, pwi, file);

        pw.close();
        pwi.close();
    }
}