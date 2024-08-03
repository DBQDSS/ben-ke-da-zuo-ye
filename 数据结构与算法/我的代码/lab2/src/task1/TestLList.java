package task1;

import java.util.List;

public class TestLList {
    public static void main(String[] args) {
        LList<Integer> list = new LList<>();

        // 测试初始化
        System.out.println("初始化之后表是否为空? " + list.Empty());
        System.out.println("此时线性表长度为：");
        System.out.println("线性表长度为：" + list.Length());

        // 测试插入
        list.ListInsert(0, 1);
        list.ListInsert(1, 1);
        list.ListInsert(2, 2);
        list.ListInsert(3, 3);
        list.ListInsert(4, 2);

        System.out.println("在插入之后，线性表为：");
        list.PrintList();

        // 测试长度
        System.out.println("线性表长度为：" + list.Length());

        // 测试按值查找
        List<Integer> loc = list.LocateList(2);
        System.out.println("线性表中值为2的元素是:" + loc);
        List<Integer> loc1 = list.LocateList(1);
        System.out.println("线性表中值为1的元素是:" + loc1);
        List<Integer> loc2 = list.LocateList(3);
        System.out.println("线性表中值为3的元素是:" + loc2);
        List<Integer> loc3 = list.LocateList(4);
        System.out.println("线性表中值为4的元素是:" + loc3);

        // 测试按位查找
        int val = list.GetList(1);
        System.out.println("线性表中位于1号位的元素为:" + val);

        // 测试删除
        int delVal = list.ListDelete(1);
        System.out.println("将要从1号位删除的元素的值为:" + delVal);
        System.out.println("删除此元素之后，线性表变为:");
        list.PrintList();

        // 测试销毁
        list.DestroyList();
        System.out.println("销毁表之后，是否为空? " + list.Empty());
    }
}
