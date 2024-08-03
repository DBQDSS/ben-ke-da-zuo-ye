package task1;

public class TestAList {
    public static void main(String[] args) {
        AList<Integer> myList = new AList<Integer>();
        myList.InitList(20);

        // 检测初始化是否成功
        System.out.println("初始的线性表状态：");
        // 测试线性表是否为空
        System.out.println("线性表表是否为空? " + myList.Empty());
        // 检测线性表长度
        System.out.println("线性表长为: " + myList.Length());

        // 测试插入函数（线性表从0开始）
        for(int i = 0; i < 9; i++) {
            myList.ListInsert(i, i+1);
        }
        myList.ListInsert(9, 1);
        myList.ListInsert(10, 1);

        // 打印表的长度
        System.out.println("插入元素之后，线性表长为：" + myList.Length());

        // 打印表中元素
        System.out.println("线性表中的元素为: ");
        myList.PrintList();

        // 测试按值查找函数，查找值为5的元素位置
        System.out.println("值为5的元素的位置为: " + myList.LocateList(5));
        System.out.println("值为1的元素的位置为: " + myList.LocateList(1));
        System.out.println("值为15的元素的位置为: " + myList.LocateList(15));

        // 测试按位查找函数，查找位置为7的元素值
        System.out.println("处于7号位的元素值为: " + myList.GetList(7));
        System.out.println("处于15号位的元素值为: " + myList.GetList(15));

        // 测试插入函数，位置为5插入值为10的元素
        myList.ListInsert(5, 10);
        System.out.println("在5号位后插入一个值为10的元素，线性表变为: ");
        myList.PrintList();

        // 测试删除函数，删除位置为8的元素
        System.out.println("8号位元素的值为: " + myList.listDelete(8));
        System.out.println("删去8号位之后，线性表变为: ");
        myList.PrintList();

        // 销毁表
        myList.DestroyList();
        System.out.println("线性表在销毁后是否为空: " + myList.Empty());
    }
}
