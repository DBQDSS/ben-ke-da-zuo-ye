package task1and2;

public class LList<T> implements List<T> {
    private Link head;
    private Link tail;
    private Link curr;

    public LList() {
        head = null;
        curr = null;
        tail = null;
    }

    @Override
    public void insert(Object newElement) {
        if (head == null) {
            head = new Link(newElement, null);
            curr = head;
            tail = head;
            return;
        }
        Link temp = new Link(newElement, curr.next());
        curr.setNext(temp);
        if (curr == tail)
            tail = temp;
        curr = temp;
    }

    @Override
    public void remove() {
        if(head != null) {
            System.out.println("the list is empty!");
            return;
        }
        if (head == curr) {
            head = head.next();
            if (this.isEmpty()) {
                curr = tail = null;
                return;
            }
            curr = head;
            return;
        }
        Link temp = head;
        while (temp.next() != curr)
            temp = temp.next();
        temp.setNext(curr.next());
        if (curr == tail) {
            curr = head;
            tail = temp;
            return;
        }
        curr = curr.next();
    }

    @Override
    public void replace(T newElement) {
        if (curr == null) return;
        curr.setElement(newElement);
    }

    @Override
    public void clear() {
        head = curr = tail = null;
    }

    @Override
    public boolean isEmpty() {
        return head == null;
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public boolean gotoBeginning() {
        if(isEmpty()) {
            System.out.println("the list is empty!");
            return false;
        }
        curr = head;
        return true;
    }

    @Override
    public boolean gotoEnd() {
        if(isEmpty()) {
            System.out.println("the list is empty!");
            return false;
        } ;
        curr = tail;
        return true;
    }

    @Override
    public boolean gotoNext() {
        if (this.isEmpty() || curr == tail) return false;
        curr = curr.next();
        return true;
    }

    @Override
    public boolean gotoPrev() {
        if (this.isEmpty() || curr == head) return false;
        Link temp = head;
        while (temp.next() != curr)
            temp = temp.next();
        curr = temp;
        return true;
    }

    @Override
    public T getCursor() {
        return (T) curr.element();
    }

    public int currCount() {
        int currNum = 0;
        Link temp = head;
        while (temp != curr) {
            temp = temp.next();
            currNum++;
        }
        return currNum;
    }

    @Override
    public void showStructure() {
        if (this.isEmpty()) {
            System.out.println("Empty list "+"{capacity = " + 512 + ", length = " + cnt() + ", cursor = " + (currCount()-1) + "}");
            return;
        }
        Link temp = head;
        while (temp != null) {
            System.out.print(temp.element());
            System.out.print(' ');
            temp = temp.next();
        }
        System.out.println("{capacity = " + 512 + ", length = " + cnt() + ", cursor = " + currCount() + "}");
    }

    @Override
    public void moveToNth(int n) throws ListException {
        if (isEmpty() || n < 0 || n >= currCount()) {
            System.out.println();
        }
        Link temp=head;
        for(int i=0;i<n;i++){
            temp=temp.next();
        }
        curr=temp;
    }

    @Override
    public Double getCurrentUsage() {
        return null;
    }

    @Override
    public boolean find(Object searchElement) throws ListException {
        if(isEmpty()){
            System.out.println("Invalid index");
        }
        Link initial=curr;
        while(curr!=null){
            curr=curr.next();
            if(curr.element()==searchElement){
                return true;
            }
            if(curr.next()==null){
                return false;
            }
        }
        return false;
    }
    public int cnt(){
        int currNum = 0;
        Link temp = head;
        while (temp != null) {
            temp = temp.next();
            currNum++;
        }
        return currNum;
    }


    public String toString() {
        StringBuilder tmpString = new StringBuilder();
        if (this.isEmpty()) {
            tmpString = new StringBuilder("Empty list {capacity = 512, length = 0, cursor = -1}");
            return tmpString.toString();
        }
        Link temp = head;
        while (temp != null) {
            tmpString.append(temp.element());
            tmpString.append(' ');
            temp = temp.next();
        }
        tmpString.append("{capacity = " + 512 + ", length = " + this.cnt() + ", cursor = " + this.currCount() + "}");
        return tmpString.toString();
    }
}
