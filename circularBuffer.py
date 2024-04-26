#!/usr/bin/env python3

class StringCircularBuffer(object):
    def __init__(self, max_size=10):
        """Initialize the CircularBuffer with a max_size if set, otherwise
        max_size will elementsdefault to 10"""
        self._buffer = [None] * max_size
        self._head = 0
        self._tail = 0
        self._max_size = max_size
        self._isFull = False
        self._isEmpty = True
        self._totalSize = 0

    def __str__(self):
        """Return a formatted string representation of this CircularBuffer."""
        items = ['{!r}'.format(item) for item in self._buffer]
        return '[' + ', '.join(items) + ']'

    def __size(self):
        """Return the size of the CircularBuffer """
        return self._totalSize

    def __front(self):
        """Return the item at the front of the CircularBuffer """
        return self._buffer[self._head]

    def is_empty(self):
        """Return True if the head of the CircularBuffer is equal to the tail,
        otherwise return False """
        return self._isEmpty

    def is_full(self):
        """Return True if the tail of the CircularBuffer is one before the head,
        otherwise return False """
        return self._isFull

    def enqueue(self, item):
        """Insert an item at the back of the CircularBuffer """
        if self._isFull:
            raise OverflowError (
                "CircularBuffer is full, unable to enqueue item"
            )
        if not isinstance(item, str):
            raise TypeError (
                "Invalid type"
            )
        
        self._buffer[self._tail] = item
        #self.tail = (self.tail + 1) % self.max_size 
        if self._isEmpty == True:
            self._isEmpty = False   
        elif (self._tail + 1) % self._max_size == self._head: 
            self._isFull = True
            
        self._tail = (self._tail + 1) % self._max_size
        # self.max_size increases by one to ease counting of the index
        self._totalSize = (self._totalSize + 1) % (self._max_size + 1)

    def dequeue(self):
        """Return the item at the front of the Circular Buffer and remove it """
        if self._isEmpty:
            raise OverflowError (
                "CircularBuffer is empty, unable to dequeue item"
            )
        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._max_size
        
        if self._isFull:
            self._isFull = False
        elif self._head == self._tail:
            self._isEmpty = True

        # self.max_size increases by one to ease counting of the index
        self._totalSize = (self._totalSize - 1) % (self._max_size + 1)
        return item
    
    def flush_content(self):
        """Flush all the content."""
        if self._isEmpty:
            return None
        
        items = b''
        items = items.join(self.dequeue().encode() for _ in range(self._totalSize))
        self.__front()
        self._tail = self._head
        return items

def main():
    rb = StringCircularBuffer(7)
    # rb.enqueue("Testing1")
    # rb.enqueue("Testing2")
    # rb.enqueue("Testing3")
    # rb.enqueue("Testing4")
    # print(rb.dequeue())
    # print(rb.dequeue())
    # print(rb.dequeue())
    # print(rb.dequeue())
    # rb.enqueue("Testing1")
    # rb.enqueue("Testing2")
    # rb.enqueue("Testing3")
    # rb.enqueue("Testing4")
    # print(rb.dequeue())
    # print(rb.dequeue())
    # print(rb.dequeue())
    # print(rb.dequeue())
    rb.enqueue("Testing1")
    rb.enqueue("Testing2")
    rb.enqueue("Testing3")
    rb.enqueue("Testing4")
    rb.enqueue("Testing5")
    rb.enqueue("Testing6")
    rb.enqueue("Testing7")
    print(rb.dequeue())
    print(rb.dequeue())
    print(rb.dequeue())
    print(rb.dequeue())
    print(rb.dequeue())
    print(rb.dequeue())
    print(rb.dequeue())

if  __name__ =='__main__':
    main()
