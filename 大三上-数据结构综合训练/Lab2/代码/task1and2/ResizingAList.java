package task1and2;

public class ResizingAList<T> implements List<T>{
    public static final int defaultsize = 1;
    public int msize;

    public int numInList;
    public int curr;
    private Object[] listArray;
    public ResizingAList(){
        this(defaultsize);
    }
    public ResizingAList(int msize){
        this.msize = msize;
        this.curr = 0;
        this.numInList = 0;
        listArray = new Object[msize];
    }
    @Override
    public void insert(T newElement) throws ListException {
        if(isFull()){
            Object[] newArray=new Object[msize*2];
            for(int i=0;i<msize;i++){
                newArray[i]=listArray[i];
            }
            listArray=newArray;
            msize=msize*2;
            insert(newElement);
        }else {
            if(this.isEmpty()){
                listArray[0] = newElement;
                numInList++;
                return;
            }
            curr++;
            for(int i = numInList; i > curr; i--)
                listArray[i] = listArray[i-1];
            listArray[curr] = newElement;
            numInList++;
        }
    }

    @Override
    public void remove() throws ListException {
        if(this.isEmpty()){
            System.out.println("List is empty");
            return;
        }
        if((curr < 0) && (curr >= numInList)) {
            System.out.println("Bad value for curr while remove");
            return;
        }
        for(int i = curr; i < numInList-1; i++)
            //前移删除位置之后的所有元素，删除元素被取代。
            listArray[i] = listArray[i+1];
        if(curr == numInList - 1)
            //被删除的是最后一个元素，指针归零。
            curr = 0;
        numInList--;
        if(numInList<=(msize/4)&&msize>1){
            Object[] newArray=new Object[msize/2];
            for(int i=0;i<numInList;i++){
                newArray[i]=listArray[i];
            }
            listArray=newArray;
            msize=msize/2;
        }
    }

    @Override
    public void replace(T newElement) throws ListException {
        if((curr < 0) && (curr >= numInList)) {
            System.out.println("Bad value for curr while replace");
            return;
        }
        listArray[curr] = newElement;
    }

    @Override
    public void clear() {
        listArray = new Object[msize];
        curr = 0;
        numInList = 0;
    }

    @Override
    public boolean isEmpty() {
        return numInList == 0;
    }

    @Override
    public boolean isFull() {
        return numInList==msize;
    }

    @Override
    public boolean gotoBeginning() {
        if(this.isEmpty()){
            return false;
        }
        curr = 0;
        return true;
    }

    @Override
    public boolean gotoEnd() {
        if(this.isEmpty())return false;
        curr = numInList - 1;
        return true;
    }

    @Override
    public boolean gotoNext() {
        if((curr >= 0)&&(curr < numInList - 1)){
            curr++;
            return true;
        }
        else return false;
    }

    @Override
    public boolean gotoPrev() {
        if((curr > 0)&&(curr < numInList)){
            curr--;
            return true;
        }
        else return false;
    }

    @Override
    public T getCursor() throws ListException {
        return (T) listArray[curr];
    }

    @Override
    public void showStructure() {
        if(this.isEmpty()){
            //空表。
            System.out.println("Empty list "+"{capacity = " + msize + ", length = " + numInList + ", cursor = " + (curr-1) + "}");
            return;
        }
        for(int i = 0; i < numInList; i++){
            //依次输出表中元素。
            System.out.print(listArray[i]);
            System.out.print(' ');
        }
        System.out.println("{capacity = " + msize + ", length = " + numInList + ", cursor = " + curr + "}");//指针位置。

    }

    @Override
    public void moveToNth(int n) throws ListException {
        if (isEmpty() || n < 0 || n >= numInList) {
            throw new ListException("Invalid index");
        }
        curr = n;
    }

    @Override
    public boolean find(T searchElement) throws ListException {
        if(isEmpty()){
            System.out.println("Invalid index");
        }
        int initial=curr;
        for(int i=initial;i<numInList;i++){
            if (listArray[i].equals(searchElement)) {
                curr=i;
                return true;
            }
        }
        curr=numInList-1;
        return false;
    }
    @Override
    public String toString(){
        StringBuilder tmpString = new StringBuilder();
        if(this.isEmpty()){
            tmpString = new StringBuilder("Empty list ");
            tmpString.append("{capacity = " + 512 + ", length = " + this.numInList + ", cursor = " + (this.curr-1) + "}");
            return tmpString.toString();
        }
        for(int i = 0; i < numInList; i++){
            tmpString.append(listArray[i]);
            tmpString.append(' ');
        }
        tmpString.append("{capacity = " + 512 + ", length = " + this.numInList + ", cursor = " + this.curr + "}");
        return tmpString.toString();
    }
    public Double getCurrentUsage() {
        return (double) numInList / msize; // 返回当前使用率
    }
}
