package task1and2;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;

public class TestListNew<T> {
    public static void wrongLine(task1and2.List wrongRecord, int line, String translatedList) throws FileNotFoundException, ListException {
        Scanner fin = new Scanner(new File("src\\task1and2\\list_testcase.txt"));
        String tmp = new String();
        for(int i = 0; i <line; i++){
            tmp = fin.nextLine();
        }
        if(!tmp.equals(translatedList)){
            wrongRecord.insert(line);
        }
    }
    public static final int FREE_TEST = 1;
    public static final int TEXT_TEST = 2;

    public static void translator(task1and2.List<Character> list, int mode, ArrayList<Double> usageData) throws FileNotFoundException, ListException {
        try{
        }finally {
            if (mode == FREE_TEST) {
                Scanner in = new Scanner(System.in);
                String temp = in.nextLine();
                while (!temp.equals("stop")) {
                    for (int i = 0; i < temp.length(); i++) {
                        switch (temp.charAt(i)) {
                            case ' ':
                                continue;
                            case '+':
                                list.insert(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '-':
                                list.remove();
                                continue;
                            case '=':
                                list.replace(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '#':
                                list.gotoBeginning();
                                continue;
                            case '*':
                                list.gotoEnd();
                                continue;
                            case '>':
                                list.gotoNext();
                                continue;
                            case '<':
                                list.gotoPrev();
                                continue;
                            case '~':
                                list.clear();
                                continue;
                            default:
                                break;
                        }
                    }
                    list.showStructure();
                    temp = in.nextLine();
                }
                in.close();
            } else if(mode == TEXT_TEST){
                task1and2.List wrong = new ResizingAList();
                int line = 1;
                Scanner fin = new Scanner(new File("src\\task1and2\\list_testcase.txt"));
                String temp = fin.nextLine();
                while (!temp.equals("stop")) {
                    for (int i = 0; i < temp.length(); i++) {
                        switch (temp.charAt(i)) {
                            case ' ':
                                continue;
                            case '+':
                                list.insert(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '-':
                                list.remove();
                                continue;
                            case '=':
                                list.replace(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '#':
                                list.gotoBeginning();
                                continue;
                            case '*':
                                list.gotoEnd();
                                continue;
                            case '>':
                                list.gotoNext();
                                continue;
                            case '<':
                                list.gotoPrev();
                                continue;
                            case '~':
                                list.clear();
                                continue;
                            default:
                                break;
                        }
                    }
                    usageData.add((list).getCurrentUsage());
                    list.showStructure();
                    wrongLine(wrong, line, list.toString());
                    line++;
                    temp = fin.nextLine();
                }
                fin.close();

                System.out.println("the followings are the wrong lines:");
                System.out.println("(showed with list just defined,the last number is index of the wrong line list, ignore it)");
                if (wrong.isEmpty()){
                    System.out.println("Nothing Wrong");
                }else {wrong.showStructure();}

            }
        }

    }
    public static void translator2(task1and2.List<Character> list, int mode, ArrayList<Double> usageData) throws FileNotFoundException, ListException {
        try{

        }finally {
            if (mode == FREE_TEST) {
                Scanner in = new Scanner(System.in);
                String temp = in.nextLine();
                while (!temp.equals("stop")) {
                    for (int i = 0; i < temp.length(); i++) {
                        switch (temp.charAt(i)) {
                            case ' ':
                                continue;
                            case '+':
                                list.insert(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '-':
                                list.remove();
                                continue;
                            case '=':
                                list.replace(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '#':
                                list.gotoBeginning();
                                continue;
                            case '*':
                                list.gotoEnd();
                                continue;
                            case '>':
                                list.gotoNext();
                                continue;
                            case '<':
                                list.gotoPrev();
                                continue;
                            case '~':
                                list.clear();
                                continue;
                            default:
                                break;
                        }
                    }
                    list.showStructure();
                    temp = in.nextLine();
                }
                in.close();
            } else if(mode == TEXT_TEST){
                Scanner fin = new Scanner(new File("src\\task1and2\\list_testcase.txt"));
                String temp = fin.nextLine();
                while (!temp.equals("stop")) {
                    for (int i = 0; i < temp.length(); i++) {
                        switch (temp.charAt(i)) {
                            case ' ':
                                continue;
                            case '+':
                                list.insert(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '-':
                                list.remove();
                                continue;
                            case '=':
                                list.replace(temp.charAt(i + 1));
                                i++;
                                continue;
                            case '#':
                                list.gotoBeginning();
                                continue;
                            case '*':
                                list.gotoEnd();
                                continue;
                            case '>':
                                list.gotoNext();
                                continue;
                            case '<':
                                list.gotoPrev();
                                continue;
                            case '~':
                                list.clear();
                                continue;
                            default:
                                break;
                        }
                    }
                    usageData.add((list).getCurrentUsage());
                    temp = fin.nextLine();
                }
                fin.close();


            }
        }

    }

    public static void main(String[] args) throws FileNotFoundException, ListException {
        task1and2.List<Character> list = new ResizingAList<>();
        List<Character> list1 = new AList<>();
        ArrayList<Double>[] usageData = new ArrayList[]{new ArrayList<>(),new ArrayList<>()};
        translator(list, TEXT_TEST, usageData[0]);
        translator2(list1, TEXT_TEST, usageData[1]);
    }
}
