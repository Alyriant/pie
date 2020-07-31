
class DoublyLinkedList:

    class Node:
        def __init__(self, val, prev=None):
            self.val = val
            self.next = None
            self.prev = prev
            
    def __init__(self):
        self.head = None
        self.tail = None
        
    def extend(self, it):
        for i in it:
            if self.tail == None:
                self.head = DoublyLinkedList.Node(i)
                self.tail = self.head
            else:
                old_tail = self.tail
                n = DoublyLinkedList.Node(i, prev=old_tail)
                old_tail.next = n
                self.tail = n
                
    def swap_alternating(self):
        """Change list B=C=D=E to C=B=E=D"""
        if self.head and self.head != self.tail:
            b = self.head
            while True:
                if b is None or b.next is None:
                    break
                # swap one pair: B=C=D -> C=B=D
                a = b.prev
                c = b.next         
                d = c.next
                if b == self.head:
                    self.head = c
                else:
                    a.next = c
                c.prev = a
                c.next = b
                b.prev = c
                b.next = d
                if d:
                    d.prev = b
                else:
                    self.tail = b
                b = d
        return self.head

    def __str__(self):
        s = "["
        n = self.head
        while n:
            s += str(n.val) + ", "
            n = n.next
        s += "]"
        return s

if __name__ == "__main__":
    dll = DoublyLinkedList()
    dll.extend([1,2,3,4,5])
    dll.swap_alternating()
    print(dll)