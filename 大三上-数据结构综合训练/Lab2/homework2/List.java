import java.io.PrintWriter;

public interface List<T> {
	void insert(T newElement) throws ListException;
	/*
	 * Precondition: List is not full and newElement is not null.
	 * PostCondition:
	 * Inserts newElement into a list after the cursor. If the list is empty,newElement is inserted as the first(and only)element in the list.
	 * In either case(empty or not empty),moves the cursor to newElement.
	 * If there is not enough space in the list, throw a ListException exception.
	 * ListException is a custom Exception class which you should define it.
	 */
	void remove();
	/*
	 * Precondition: 
	 * List is not empty.
	 * PostCondition:
	 * Removes the element marked by the cursor from a list.If the resulting list is not empty,
	 * then moves the cursor to the element that followed the deleted element.If the deleted element
	 * was at the end of the list,then moves the cursor to the element at the beginning of the list.
	 *
	 */
	void replace(T newElement);
	/*
	 * Precondition: 
	 * List is not empty and newElement is not null.
	 * PostCondition:
	 * Replaces the element marked by the cursor with newElement. The cursor remains at newElement.
	 */
	void clear();
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * Removes all the elements in a list.
	 */
	boolean isEmpty();
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * Returns true if a list is empty. Otherwise , returns false.
	 */
	boolean isFull();
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * Returns true if a list is full. Otherwise, returns false.
	 */
	boolean gotoBeginning();
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * If a  list is not empty, then moves the cursor to the beginning of
	 * the list and returns true.Otherwise,returns false.
	 */
	boolean gotoEnd();
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * If a list is not empty,then moves the cursor to the end of the list 
	 * and returns true.Otherwise, returns false.
	 */
	boolean gotoNext();
	/*
	 * Precondition: 
	 * List is not empty.
	 * PostCondition:
	 * If the cursor is not at the end of a list,then moves the cursor to the
	 * next element in the list and return true.Otherwise,returns false.
	 */
	boolean gotoPrev();
	/*
	 * Precondition: 
	 * List is not empty.
	 * PostCondition:
	 * If the cursor is not at the beginning of a list,then moves the cursor to
	 * the preceding element in the list and returns true.Otherwise,returns false.
	 */
	T getCursor();
	/*
	 * Precondition: 
	 * List is not empty.
	 * PostCondition:
	 * Returns a copy of the element marked by the cursor.
	 */
	void showStructure(PrintWriter pw);
	/*
	 * Precondition: 
	 * None
	 * PostCondition:
	 * Outputs the elements in a list and the value of cursor. If the list is empty,outputs "Empty list".
	 * Note that this operation is intended for testing/debugging purpose only.
	 */
	void moveToNth(int n);
	/*
	 * Precondition: 
	 * List contains at least n + 1 elements.
	 * Postcondition:
	 * Removes the element marked by the cursor from a list and reinserts it as the nth element in the list, where the elements are numbered from beginning to end, starting with zero. Moves the cursor to the moved element. 
	 */
	boolean find(T searchElement);
	/*
	 * Precondition:
	 * List is not empty.
	 * Postcondition:
	 * Searches a list for searchElement. Begins the search with the element marked by the cursor. Moves the cursor through the list until either searchElement is found (returns true) or the end of the list is reached without finding searchElement (returns false). Leaves the cursor at the last element visited during the search.
	 */
}
