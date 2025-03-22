package task1and2;

public class BinNode <K extends Comparable<K>, V> {

    //设置二叉树的单个节点
    public K key;//键
    public V value;//值
    private BinNode<K,V> left;//左节点
    private BinNode<K,V> right;//右节点
    public BinNode(){
        this(null,null);
    }
    public BinNode(K key, V value){
        this.key = key;
        this.value = value;
    }
    public BinNode(BinNode<K,V> p){
        this.key = p.key();
        this.value = p.value();
        this.left = p.left();
        this.right = p.right();
    }
    public K key(){
        return key;
    }
    public V value(){
        return value;
    };
    public void setKey(K key){
        this.key = key;
    }
    public void setValue(V value){
        this.value = value;
    };
    //新的修改值的方法
    public void setValue1(V value){
        ((StringBuilder)(this.value)).append(" ").append(value);
    };

    public BinNode<K,V> left(){ return left; };
    public BinNode<K,V> setLeft(BinNode<K,V> p){return this.left = p; };

    public BinNode<K,V> right(){ return right; };
    public BinNode<K,V> setRight(BinNode<K,V> p){return this.right = p; };

    public boolean isLeaf(){return left == null && right == null; };//判断是否是叶子节点
}
