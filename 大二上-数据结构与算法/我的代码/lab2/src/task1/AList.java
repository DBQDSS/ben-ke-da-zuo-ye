package task1;

import java.util.ArrayList;
import java.util.List;

public class AList<E> {
    private int defaultSize = 10; // 默认容量
    private E[] list; // 数组，用于存放元素
    private int size = 0; // 当前表长度

    // 初始化线性表
    public void InitList() {
        this.list = (E[]) new Object[defaultSize];
        this.size = 0;
    }

    public void InitList(int len) {
        this.list = (E[]) new Object[len];
        this.size = 0;
    }

    // 销毁线性表
    public void DestroyList() {
        list = null;
        size = 0;
    }

    // 获取线性表长度
    public int Length() {
        return size;
    }

    // 判断线性表是否为空
    public boolean Empty() {
        return size == 0;
    }

    // 打印表中元素
    public void PrintList() {
        for(int i = 0; i < size; i++) {
            System.out.print(list[i]);
            System.out.print(" ");
        }
        System.out.println();
    }

    // 按值查找元素位置
    public List<Integer> LocateList(E e) {
        List<Integer> positions = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            if (list[i].equals(e)) {
                positions.add(i);
            }
        }
        return positions;
    }

    // 按位查找元素
    public E GetList(int i) {
        if(i >= 0 && i < size) {
            return list[i];
        }else {
            System.out.println("查找位置无效");
            return null;
        }
    }

    // 在指定位置插入元素
    public void ListInsert(int i, E e) {
        if(i < 0 || i > size) {
            System.out.println("插入位置无效");
            return;
        }
        if(size == list.length) {
            System.out.println("表已满，无法插入");
            return;
        }
        for(int j = size; j > i; j--) {
            list[j] = list[j-1];
        }
        list[i] = e;
        size++;
    }

    // 删除指定位置元素
    public E listDelete(int i) {
        if(i < 0 || i >= size) {
            System.out.println("删除位置无效");
            return null;
        }
        E deletedElement = list[i];
        for(int j = i; j < size - 1; j++) {
            list[j] = list[j+1];
        }
        size--;
        return deletedElement;
    }
}

