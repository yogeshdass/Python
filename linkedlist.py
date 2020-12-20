#!/usr/bin/python3

class Girl(object):
    def __init__(self, name):
        self.name = name
        self.girlNextDoor = None

class GirlsLinkedList(object):
    def __init__(self):
        self.head = None

    def printList(self):
        #print(self.head.name)
        #print(self.head.girlNextDoor)
        #print(self.head.girlNextDoor.name)
        pointerHead = self.head
        while pointerHead:
            print(F"{pointerHead.name} | { hex(id(pointerHead.girlNextDoor))}, ", end="")
            pointerHead = pointerHead.girlNextDoor
        print()

    def insertAtBeginning(self, Girl):
        Girl.girlNextDoor = self.head
        self.head = Girl

    def insertAtEnd(self, Girl):
        pointerHead = self.head
        lastGirl = self.head
        while pointerHead:
            lastGirl = pointerHead
            pointerHead = pointerHead.girlNextDoor
        lastGirl.girlNextDoor = Girl

    def insertAfter(self, newGirl, afterGirl):
        pointerHead = self.head
        while pointerHead:
            if pointerHead  is afterGirl:
                newGirl.girlNextDoor = afterGirl.girlNextDoor
                afterGirl.girlNextDoor = newGirl
            pointerHead = pointerHead.girlNextDoor
    
    def delGirl(parameter_list):
        pass
    def delAtPos(parameter_list):
        pass
    def searchGirl(parameter_list):
        pass
            
if __name__ == "__main__":
    ll = GirlsLinkedList()
    n1 = Girl(1)
    n2 = Girl(2)
    n3 = Girl(3)
    #ll.head = n1

    print(n1)
    print(n2)
    print(n3)
    #print(ll.head)
    #print(ll)

    n1.girlNextDoor = n2
    n2.girlNextDoor = n3
    ll.head = n1
    print(ll.head)
    print(ll)
    print(n1.girlNextDoor)
    print(n2.girlNextDoor)
    print(n3.girlNextDoor)
    
    ll.printList()
    ll.insertAtBeginning(Girl("A"))
    ll.insertAtEnd(Girl("Z"))
    ll.printList()
    ll.insertAfter(Girl("X"), n1)
    ll.printList()