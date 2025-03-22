package task1;

import java.util.*;
public class LList<E> {
    Node<E> head;
    int size;

    // 初始化链表
    public LList() {
        head = null;
        size = 0;
    }

    // 销毁链表
    public void DestroyList() {
        head = null;
        size = 0;
    }

    // 返回链表长度
    public int Length() {
        return size;
    }

    // 判断链表是否为空
    public boolean Empty() {
        return size == 0;
    }

    // 输出链表元素
    public void PrintList() {
        Node<E> temp = head;
        while (temp != null) {
            System.out.print(temp.data);
            System.out.print(" ");
            temp = temp.next;
        }
        System.out.println();
    }

    // 按值查找元素位置
    public List<Integer> LocateList(E e) {
        List<Integer> result = new ArrayList<>();
        Node<E> temp = head;
        int index = 0;
        while (temp != null) {
            if (temp.data.equals(e)) {
                result.add(index);
            }
            temp = temp.next;
            index++;
        }
        return result;
    }

    // 按位查找元素
    public E GetList(int i) {
        if (i < 0 || i >= size) {
            throw new IndexOutOfBoundsException("索引超出范围!");
        }
        Node<E> temp = head;
        for (int j = 0; j < i; j++) {
            temp = temp.next;
        }
        return temp.data;
    }

    // 在第i个位置插入元素e
    public void ListInsert(int i, E e) {
        if (i < 0 || i > size) {
            throw new IndexOutOfBoundsException("索引超出范围!");
        }
        Node<E> newNode = new Node<>(e);
        if (i == 0) {
            newNode.next = head;
            head = newNode;
        } else {
            Node<E> prev = head;
            for (int j = 0; j < i - 1; j++) {
                prev = prev.next;
            }
            newNode.next = prev.next;
            prev.next = newNode;
        }
        size++;
    }

    // 删除第i个位置的元素，并返回其值
    public E ListDelete(int i) {
        if (i < 0 || i >= size) {
            throw new IndexOutOfBoundsException("索引超出范围!");
        }
        Node<E> removedNode;
        if (i == 0) {
            removedNode = head;
            head = head.next;
        } else {
            Node<E> prev = head;
            for (int j = 0; j < i - 1; j++) {
                prev = prev.next;
            }
            removedNode = prev.next;
            prev.next = removedNode.next;
        }
        size--;
        return removedNode.data;
    }
}
