package forth.queue;

import forth.list.ListException;

public interface DQueue<T> {
    public boolean isEmpty();
    /*
     * Precondition: None
     * Postcondition:
     * Return true if dqueue is not empty.
     * Return false if dequeu has not any element.
     */
    public boolean isFull();
    /*
     * Precondition: None
     * Postcondition:
     * Return true if dqueue is full.
     * Return false if dequeue is not full.
     */
    public int size();
    /*
     * Precondition: None
     * Postcondition:
     * Return the number of elemnts in the queue,otherwise return 0 if the queue is empty.
     */
    void enqueueToRear(T element) throws ListException;
    /*
     * Precondition: DQueue is not full and element is not null.
     * Postcondition:
     * Inserts element into the rear of this queue.
     * If there is not enough space in the queue,throw a ListException exception.
     */
    void enqueueToFront(T element) throws ListException;
    /*
     * Precondition: DQueue is not full and element is not null.
     * Postcondition:
     * Inserts element into the front of this queue.
     * If there is not enough space in the queue,throw a ListException exception.
     */
    T dequeueFromFront();
    /*
     * Precondition: DQueue is not empty.
     * Postcondition:
     * Delete element front the front of this queue and return it.
     * If the queue is empty, return null.
     */
    T dequeueFromRear();
    /*
     * Precondition: DQueue is not empty.
     * Postcondition:
     * Delete element front the rear of this queue and return it.
     * If the queue is empty, return null.
     */
    T getFront();
    /*
     * Precondition: None
     * Postcondition:
     * Return null if the queue is empty.
     * Return the element which is the front of the queue.
     */
    T getRear();
    /*
     * Precondition: None
     * Postcondition:
     * Return null if the queue is empty.
     * Return the element which is the rear of the queue.
     */
}
