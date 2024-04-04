#!/usr/bin/env python3

class StringCircularBuffer(object):

    def __init__(self, max_size=10):
        """Initialize the CircularBuffer with a max_size if set, otherwise
        max_size will elementsdefault to 10"""
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.max_size = max_size
        self.isFull = False
        self.isEmpty = True
        self.totalSize = 0

    def __str__(self):
        """Return a formatted string representation of this CircularBuffer."""
        items = ['{!r}'.format(item) for item in self.buffer]
        return '[' + ', '.join(items) + ']'

    def size(self):
        """Return the size of the CircularBuffer """
        return self.totalSize

    def is_empty(self):
        """Return True if the head of the CircularBuffer is equal to the tail,
        otherwise return False """
        return self.isEmpty

    def is_full(self):
        """Return True if the tail of the CircularBuffer is one before the head,
        otherwise return False """
        return self.isFull

    def enqueue(self, item):
        """Insert an item at the back of the CircularBuffer """
        if self.isFull:
            raise OverflowError (
                "CircularBuffer is full, unable to enqueue item"
            )
        #if not isinstance(item, str):
        #    raise TypeError (
        #        "Invalid type"
        #    )
        
        self.buffer[self.tail] = item
        #self.tail = (self.tail + 1) % self.max_size 
        if self.isEmpty == True:
            self.isEmpty = False   
        elif (self.tail + 1) % self.max_size == self.head: 
            self.isFull = True
            
        self.tail = (self.tail + 1) % self.max_size
        # self.max_size increases by one to ease counting of the index
        self.totalSize = (self.totalSize + 1) % (self.max_size + 1)

    def front(self):
        """Return the item at the front of the CircularBuffer """
        return self.buffer[self.head]

    def dequeue(self):
        """Return the item at the front of the Circular Buffer and remove it """
        if self.isEmpty:
            raise OverflowError (
                "CircularBuffer is empty, unable to dequeue item"
            )
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.max_size
        
        if self.isFull:
            self.isFull = False
        elif self.head == self.tail:
            self.isEmpty = True

        # self.max_size increases by one to ease counting of the index
        self.totalSize = (self.totalSize - 1) % (self.max_size + 1)
        return item
    
    def flush_content(self):
        """Flush all the content."""

        if self.isEmpty:
            return None
        
        items = b''
        items = items.join(self.dequeue().encode() for _ in range(self.totalSize))
        self.front()
        self.tail = self.head
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
