#!/usr/bin/python3
import random
import sys

class Skiplist:
    def __init__(self):
        #The main point of the skiplist object, other than defining functions for
        #manipulation of the nodes, is maintaining a head pointer.
        self.head = None
    

    '''
        From a deleted node "delnode", stitches together the prev and next nodes
        accordingly while clearing out dead ptrs.
    '''
    def __stitch__(self, delnode):
        if delnode.prevs is None:
            delnode.nexts.reverse()
            newhead = delnode.nexts.pop()
            for i in range(delnode.levels - newhead.levels):
                newhead.nexts.append(delnode.nexts.pop())
                    
            #Head never has any prevs since it's the head.
            newhead.prevs = None
            self.head = newhead
        elif all(map(lambda x: x is None, delnode.nexts)):
            for i in range(len(delnode.prevs)):
                delnode.prevs[i].next = None
                delnode.prevs[i] = None
        else:
            for i in range(len(delnode.prevs)):
                delnode.prevs[i].nexts[i] = delnode.nexts[i]
                if delnode.nexts[i] is not None:
                    delnode.nexts[i].prevs[i] = delnode.prevs[i]
                delnode.prevs[i] = None
                delnode.nexts[i] = None

    '''
        Proper algorithm for inserting a node at the head, tail, or otherwise,
        at the specified level for operations not involving new heads, default
        is the "ground" level, 0.
    '''
    def __insert__(self, lnode, mnode, rnode, level=0):
        if rnode is self.head: #insertion before the head. new head defined.
           #Move the previous head nexts to the new node mnode. clear old ptrs.
           mnode.nexts = [rnode] + rnode.nexts[1:]
           rnode.nexts[1:] = [None] * len(rnode.nexts[1:])
           mnode.levels = rnode.levels
           rnode.levels = 1
           self.head = mnode
           mnode.prevs[:] = [None] * len(mnode.prevs)
           mnode.prevs = None
        elif rnode is None: #insertion after the tail.
            lnode.nexts[level] = mnode
            mnode.prevs[level] = lnode
        else: #insertion in between two other nodes.
            lnode.nexts[level] = mnode
            mnode.prevs[level] = lnode
            rnode.prevs[level] = mnode
            mnode.nexts[level] = rnode

    '''
        Returns a pointer to the first node found with the requested target value.
    '''
    def __find__(self, target: int) -> object:
        curr = self.head
        level = self.head.levels - 1
        # Only case where we directly compare curr with the target.
        # This is because we are inspecting the next element otherwise.
        if curr is None:
            print("Empty list!")
            return None
        if target < curr.num:
            return None
        elif target == curr.num:
            return curr

        while curr is not None and level >= 0:
            n = curr.nexts[level]
            while n is None and level >= 0:
                level -= 1
                n = curr.nexts[level]
            if n is None:
                break
            if n.num == target:
                return n
            elif n.num < target:
                curr = n
            else:
                level -= 1
        return None
       
    def search(self, target: int) -> bool:
        node = self.__find__(target)
        if node is None:
            return False
        else:
            return True

    def add(self, num: int) -> None:
        newnode = Node(num)
        if self.head is None:
            self.head = newnode
            return None
        curr = self.head
        level = self.head.levels - 1
        prevs = [None] * self.head.levels
        inserted = False

        while inserted == False:
            if curr is None and level == 0:
                self.__insert__(prevs[level], newnode, curr)
                inserted = True
            elif num <= curr.num:
                if level > 0:
                    prevs[level] = curr
                    level -= 1
                    curr = curr.nexts[level]
                else:
                    self.__insert__(prevs[level], newnode, curr)
                    inserted = True
            else:
                prevs[level] = curr
                while curr.nexts[level] is None and level >= 1:
                    level -= 1
                    prevs[level] = curr
                curr = curr.nexts[level]
            
        

    def erase(self, num: int) -> bool:
        delnode = self.__find__(num)
        if delnode is not None:
            self.__stitch__(delnode)
            return True
        return False

    def printList(self):
        for i in range(len(self.head.nexts)):
            curr = self.head
            while curr is not None:
                sys.stdout.write('{} '.format(curr.num))
                curr = curr.nexts[i]
            print()
        print('-' * 25)
            

#Nodes for the skiplist
class Node:
    def __init__(self, num, levels=1):
        self.nexts = [None] * levels
        self.prevs = [None] * levels
        self.num = num
        self.levels = levels
