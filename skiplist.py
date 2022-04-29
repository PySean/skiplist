#!/usr/bin/python3
import random
import sys

class Skiplist:
    def __init__(self):
        #The main point of the skiplist object, other than defining functions for
        #manipulation of the nodes, is maintaining a head pointer.
        self.head = None

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
    def __init__(self, num, levels):
        self.nexts = [None] * levels
        self.num = num
