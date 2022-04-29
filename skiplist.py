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
        # we are at the very beginning.
        if self.head is None:
            self.head = Node(num, 1)
            return
        curr = self.head
        level = len(self.head.nexts) - 1
        prevs = [None] * len(self.head.nexts) #array holding last seen node per level.
                                     #keeps us from having to use prev ptrs and makes
                                     #for less traversals.
        
        #Corner case: num is a lesser or equal value to the head. Make num the new head.
        while True:
            if curr is None or num <= curr.num:
                newNode = Node(num, len(self.head.nexts))
                if curr is self.head:
                    newNexts = curr.nexts[:]
                    newNexts[0] = curr
                    newNode.nexts = newNexts
                    curr.nexts[1:] = [None] * (len(curr.nexts) - 1)
                    self.head = newNode
                    return #we set up everything for head accordingly. There is
                           #no need for promotion - does not make sense for a head insertion.
                #coin flip time
                for i in range(level, -1, -1):
                    if prevs[i] is None:
                        prevplus = prevs[i+1]
                        currkar = prevplus
                        while currkar.num <= num:
                            print('prevp: {}'.format(prevplus.num))
                            print('curkar: {}'.format(currkar.num))
                            prevplus = currkar
                            currkar = prevplus.nexts[i]
                        prevs[i] = prevplus

                newNode.nexts[0] = prevs[0].nexts[0]
                prevs[0].nexts[0] = newNode
                level = 0
                while random.randint(0,1) == 1:
                    level += 1
                    # Need to traverse all nodes and extend nexts.
                    if level > len(self.head.nexts) - 1:
                        begin = self.head
                        while begin is not None:
                            begin.nexts.append(None)
                            begin = begin.nexts[0]
                        self.head.nexts[level] = newNode
                    else:
                        newNode.nexts[level] = prevs[level].nexts[level]
                        prevs[level].nexts[level] = newNode
                return
            else:
                #print('curr num: {}, num being inserted: {}'.format(curr.num, num))
                prevs[level] = curr
                while curr.nexts[level] is None and level > 0:
                    #print("curr is {} and level is {}".format(curr.num, level))
                    level -= 1
                    prevs[level] = curr
                curr = curr.nexts[level]

    def erase(self, num: int) -> bool:
        pass

    def printero(self):
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
