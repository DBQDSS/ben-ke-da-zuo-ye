package task1and2;

import java.io.IOException;
import java.io.PrintWriter;

public class BST <K extends Comparable<K>, V>{
    private BinNode<K,V> root;

    private int numNode;//节点个数

    //插入方法的实现
    public void insert(K key, V value){
        assert(key!= null)&&(value!=null):"Wrong input";
        root=inserthelp(root,key,value);
    }

    public BinNode<K, V> inserthelp(BinNode<K,V> rt, K key, V value){
        if(rt == null) {
            numNode++;
            return new BinNode<K,V>(key, value);
        }
        if(rt.key().compareTo(key) > 0)
            rt.setLeft(inserthelp(rt.left(), key, value));
        else if(rt.key().compareTo(key) < 0)
            rt.setRight(inserthelp(rt.right(), key, value));
        else updatehelp(rt, key, value);
        return rt;
    }

    //删除方法的实现
    public V remove(K key){
        assert key != null : "Key is null.";
        assert numNode != 0 : "Tree is empty.";
        BinNode<K,V> temp = new BinNode<K,V>();
        root = removehelp(root, key, temp);
        return temp.value();
    }

    private BinNode<K,V> removehelp(BinNode<K,V> root, K key, BinNode<K,V> ans) {
        if(root==null){
            return null;
        }
        if(root.key().compareTo(key) > 0)//在左子树中递归操作
            root.setLeft(removehelp(root.left(), key, ans));
        else if(root.key().compareTo(key) < 0)//在右子树中递归操作
            root.setRight(removehelp(root.right(), key, ans));
        else {
            //找到对应键值后的操作
            ans.setValue(root.value);
            if(root.left()==null){
                root=root.right();
            } else if (root.right()==null) {
                root=root.left();
            }else {
                BinNode<K,V> temp = getmin(root.right());
                root.setKey(temp.key());
                root.setValue(temp.value());
                root.setRight(deletemin(root.right()));
            }
            numNode--;
        }
        return root;
    }

    private BinNode<K,V> deletemin(BinNode<K,V> rt) {
        if(rt.left() == null)
            // 左树为空，没有更小的结点了，找到了这棵树的最小值结点，
            // 返回它的右子树（它是null或是二叉树无影响）
            return rt.right();
        else{
            // 继续进行寻找
            rt.setLeft(deletemin(rt.left()));
            return rt;
        }
    }

    private BinNode<K, V> getmin(BinNode<K, V> rt) {
        if(rt.left() == null)
            // 左树为空，没有更小的结点了
            return new BinNode<K,V>(rt);
        else return getmin(rt.left());// 继续寻找
    }

    //查找
    public V search(K key){
        assert key != null : "Key is null.";
        return searchhelp(root, key);
    }

    private V searchhelp(BinNode<K,V> root, K key) {
        if(root == null) return null;
        if(root.key().compareTo(key) > 0)
            return searchhelp(root.left(), key);
        else if(root.key().compareTo(key) < 0)
            return searchhelp(root.right(), key);
        else
            return root.value();
    }

    //替换方法的实现
    public boolean update(K key, V value){
        assert (key != null) && (value != null) : "Wrong input.";
        return updatehelp(root, key, value);
    }
    private boolean updatehelp(BinNode<K,V> root, K key, V value) {
        if(root==null){
            return false;
        }
        if(root.key().compareTo(key)>0){
            return updatehelp(root.left(), key, value);
        }else if(root.key().compareTo(key)<0){
            return updatehelp(root.right(), key, value);
        }else {
            root.setValue(value);
        }
        return true;
    }


    public boolean isEmpty(){
        return root == null;
    };
    public void clear(){
        numNode = 0;
        root = null;
    }
    public int getHeight(BinNode<K,V> rt){
        if(rt==null){
            return 0;
        }else {
            int left;
            int right;
            left=getHeight(rt.left());
            right=getHeight(rt.right());
            return Math.max(left,right)+1;
        }
    }


    public void showStructure1(){
        System.out.println("There are " + numNode + " nodes in this BST.");
        System.out.println("The height of this BST is " + getHeight(root) + ".");
    }
    public void showStructure(PrintWriter pw) throws IOException {
        pw.println("-----------------------------");
        pw.println("There are " + numNode + " nodes in this BST.");
        pw.println("The height of this BST is " + getHeight(root) + ".");
        pw.println("-----------------------------");
        System.out.println("-----------------------------");
        System.out.println("There are " + numNode + " nodes in this BST.");
        System.out.println("The height of this BST is " + getHeight(root) + ".");
        System.out.println("-----------------------------");
    }
    public void printInorder1(){
        printhelp1(root);
    }
    private void printhelp1(BinNode<K,V> rt){
        if(rt == null) return;
        printhelp1(rt.left());
        System.out.print("[");
        System.out.print(rt.key());
        System.out.print(" --- < ");
        System.out.print(rt.value());
        System.out.println(" >]");
        printhelp1(rt.right());
    }
    public void printInorder(PrintWriter pw) throws IOException{
        printhelp(root, pw);
    }
    private void printhelp(BinNode<K,V> rt, PrintWriter pw) throws IOException{
        if(rt == null) return;
        printhelp(rt.left(), pw);
        pw.print("[");
        pw.print(rt.key());
        pw.print(" --- < ");
        pw.print(rt.value());
        pw.println(" >]");
        printhelp(rt.right(), pw);
    }


    //新插入方法的实现
    public void insert1(K key, V value){
        assert(key!= null)&&(value!=null):"Wrong input";
        root=inserthelp1(root,key,value);
    }

    public BinNode<K, V> inserthelp1(BinNode<K,V> rt, K key, V value){
        if(rt == null) {
            numNode++;
            return new BinNode<K,V>(key, value);
        }
        if(rt.key().compareTo(key) > 0)
            rt.setLeft(inserthelp1(rt.left(), key, value));
        else if(rt.key().compareTo(key) < 0)
            rt.setRight(inserthelp1(rt.right(), key, value));
        else updatehelp1(rt, key, value);
        return rt;
    }

    //新替换方法的实现
    private boolean updatehelp1(BinNode<K,V> root, K key, V value) {
        if(root==null){
            return false;
        }
        if(root.key().compareTo(key)>0){
            return updatehelp1(root.left(), key, value);
        }else if(root.key().compareTo(key)<0){
            return updatehelp1(root.right(), key, value);
        }else {
            root.setValue1(value);
        }
        return true;
    }
}
