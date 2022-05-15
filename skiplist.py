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
            newhead = delnode.nexts[0]
            if len(delnode.nexts) > len(newhead.nexts):
                for node in delnode.nexts[len(newhead.nexts):]:
                    newhead.nexts.append(node)
                delnode.nexts[:] = [None] * len(delnode.nexts)
                delnode.nexts = None
            for i in range(len(newhead.prevs)):
                newhead.prevs[i] = None
                    
            #Head never has any prevs since it's the head.
            newhead.prevs = None
            self.head = newhead
        elif all(map(lambda x: x is None, delnode.nexts)):
            for i in range(len(delnode.prevs)):
                delnode.prevs[i].nexts[i] = None
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
            #reassign the prevs of our head's nexts to the new head.
            for i in range(1, rnode.levels):
                if rnode.nexts[i] is not None:
                    rnode.nexts[i].prevs[i] = mnode
            rnode.nexts[1:] = [None] * len(rnode.nexts[1:])
            rnode.nexts = [rnode.nexts[0]]
            mnode.levels = rnode.levels
            rnode.levels = 1
            self.head = mnode
            #mnode.prevs[:] = [None] * len(mnode.prevs)
            mnode.prevs = None
            rnode.prevs = [mnode]
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
                    #curr = curr.nexts[level]
                else:
                    if curr is not self.head:
                        theprev = curr.prevs[level]
                    else:
                        theprev = prevs[level]
                    self.__insert__(theprev, newnode, curr)
                    inserted = True
            else:
                prevs[level] = curr
                while (curr.nexts[level] is None or num < curr.nexts[level].num) and level >= 1:
                    level -= 1
                    prevs[level] = curr
                if curr.nexts[level] is None or num >= curr.nexts[level].num or level == 0:
                    curr = curr.nexts[level]
                
        #Level up.
        while random.randint(0, 1) == 1:
             level += 1
             newnode.levels += 1
             if level > self.head.levels - 1:
                self.head.levels += 1
                if newnode is not self.head:
                    self.head.nexts.append(newnode)
                    newnode.prevs.append(self.head)
                    newnode.nexts.append(None)
                else:
                    self.head.nexts.append(None)
             else:
                if newnode is not self.head:
                    newnode.prevs.append(None)
                    newnode.nexts.append(None)
                    newnode.prevs[level] = prevs[level]
                    newnode.nexts[level] = prevs[level].nexts[level]
                    if prevs[level].nexts[level] is not None:
                        prevs[level].nexts[level].prevs[level] = newnode
                    prevs[level].nexts[level] = newnode
                else:
                    newnode.nexts.append(None)
        print('added {}'.format(num))
    def erase(self, num: int) -> bool:
        val = False
        delnode = self.__find__(num)
        if delnode is not None:
            self.__stitch__(delnode)
            val = True
        if val == True:
            print('erased {}'.format(num))
        else:
            print('{} not found'.format(num))
        return val

    def printList(self, backwalk=False):
        forwards = ''
        backwards = ''
        for i in range(len(self.head.nexts)):
            curr = self.head
            prev = curr
            while curr is not None:
                forwards += '{} '.format(curr.num)
                #sys.stdout.write('{} '.format(curr.num))
                prev = curr
                curr = curr.nexts[i]
            #print()
            forwards += '\n'
            if backwalk == True:
                #print('Reverse')
                while prev is not None:
                    backwards += '{} '.format(prev.num)
                    #sys.stdout.write('{} '.format(prev.num))
                    if prev.prevs is not None:
                        try:
                            prev = prev.prevs[i] 
                        except IndexError as I:
                            print(I)
                            print(forwards)
                            print('-' * 25)
                            print(backwards)
                            return
                    else:
                        prev = None
                #sys.stdout.write('{} '.format(prev.num))
                #print()
                backwards += '\n'
        sys.stdout.write(forwards)
        print('-' * 25)
        if backwalk == True:
            sys.stdout.write(backwards)
            print('-' * 25)

            

#Nodes for the skiplist
class Node:
    def __init__(self, num, levels=1):
        self.nexts = [None] * levels
        self.prevs = [None] * levels
        self.num = num
        self.levels = levels
