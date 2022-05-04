#!/usr/bin/python3
import random
import sys

class Skiplist:
    def __init__(self):
        #The main point of the skiplist object, other than defining functions for
        #manipulation of the nodes, is maintaining a head pointer.
        self.head = None
    

    '''
        From a deleted node "delnode" stitches together the prevs and nexts accordingly.
        NOTE: Can this be modified to also account for head insertions?
    '''
    def __stitch__(self, delnode):
        prevs = delnode.prevs
        nexts = delnode.nexts
        if prevs is None:
            levels = self.head.levels
            self.head = nexts[-1]
            for i in range(levels - self.head.levels):
                self.head.nexts.append(None)
            #Head never has any prevs since it's the head.
            self.head.prevs = None
        elif all(lambda x: x is None, nexts):
            for i in range(len(prevs)):
                prevs[i].next = None
        else:
            for i in range(len(prevs)):
                prevs[i].next = nexts[i]
                if nexts[i] is not None:
                    nexts[i].prevs[i] = prevs[i]

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
        elif rnode is None: #insertion after the tail.
            lnode.nexts[level] = mnode
            mnode.prevs[level] = lnode
        else #insertion in between two other nodes.
            lnode.nexts[level] = mnode
            mnode.prevs[level] = lnode
            rnode.prevs[level] = mnode
            mnode.nexts[level] = rnode


    def search(self, target: int) -> bool:
        curr = self.head
        level = len(self.head.nexts) - 1
        # Only case where we directly compare curr with the target.
        # This is because we are inspecting the next element otherwise.
        if target < curr.num:
            return False
        elif target == curr.num:
            return True

        while curr is not None and level > 0:
            n = curr.nexts[level]
            while n is None and level > 0:
                level -= 1
                n = curr.nexts[level]
            if n is None:
                break
            if n.num == target:
                return True
            elif n.num < target:
                curr = n
            else:
                level -= 1
        return False

    def add(self, num: int) -> None:
        pass

    def erase(self, num: int) -> bool:
        pass

    def printList(self):
        for i in range(len(self.head.nexts) - 1, -1, -1):
            curr = self.head
            while curr is not None:
                sys.stdout.write('{} '.format(curr.num))
                curr = curr.nexts[i]
            print()
            

#Nodes for the skiplist
class Node:
    def __init__(self, num, levels=1):
        self.nexts = [None] * levels
        self.num = num
        self.levels = levels
