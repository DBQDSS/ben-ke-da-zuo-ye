package task1and2;

public class DList<T> implements List<T> {
    private DLink head;
    private DLink tail;
    private DLink curr;

    public DList() {
        head = null;
        curr = null;
        tail = null;
    }

    @Override
    public void insert(Object newElement) {
        if (head == null) {
            head = new DLink(newElement, null, null);
            curr = head;
            tail = head;
            return;
        }
        if (curr == tail) {
            DLink temp = new DLink(newElement, curr, null);
            curr.setNext(temp);
            tail = temp;
            curr = temp;
        } else {
            DLink temp = new DLink(newElement, curr, curr.next());
            curr.setNext(temp);
            temp = temp.next();
            temp.setPrev(curr.next());
            curr = curr.next();
        }
    }

    @Override
    public void remove() {
        assert head != null : "The list is empty!";
        if (head == curr) {
            head = head.next();
            if (this.isEmpty()) {
                curr = tail = null;
                return;
            }
            head.setPrev(null);
            curr = head;
            return;
        }
        if (curr == tail) {
            tail = curr.prev();
            tail.setNext(null);
            curr = head;
        } else {
            curr.next().setPrev(curr.prev());
            curr.prev().setNext(curr.next());
            curr = curr.next();
        }
    }

    @Override
    public void replace(Object newElement) {
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
        assert !this.isEmpty() : "the list is empty!";
        curr = head;
        return true;
    }

    @Override
    public boolean gotoEnd() {
        assert !this.isEmpty() : "the list is empty!";
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
        curr = curr.prev();
        return true;
    }

    @Override
    public T getCursor() {
        return (T) curr.element();
    }

    public int currCount() {
        int currNum = 0;
        DLink temp = head;
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
        DLink temp = head;
        while (temp != null) {
            System.out.print(temp.element());
            System.out.print(' ');
            temp = temp.next();
        }
        int currNum = currCount();
        System.out.println("{capacity = " + 512 + ", length = " + cnt() + ", cursor = " + currCount() + "}");

    }

    private int cnt() {
        int currNum = 0;
        DLink temp = head;
        while (temp != null) {
            temp = temp.next();
            currNum++;
        }
        return currNum;
    }

    @Override
    public void moveToNth(int n) throws ListException {

    }

    @Override
    public Double getCurrentUsage() {
        return null;
    }

    @Override
    public boolean find(Object searchElement) throws ListException {
        return false;
    }

    public String toString() {
        StringBuilder tmpString = new StringBuilder();
        if (this.isEmpty()) {
            tmpString = new StringBuilder("Empty list {capacity = 512, length = 0, cursor = -1}");
            return tmpString.toString();
        }
        DLink temp = head;
        while (temp != null) {
            tmpString.append(temp.element());
            tmpString.append(' ');
            temp = temp.next();
        }
        tmpString.append("{capacity = " + 512 + ", length = " + this.cnt() + ", cursor = " + this.currCount() + "}");
        return tmpString.toString();
    }
}
