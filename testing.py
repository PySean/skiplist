#!/usr/bin/env python3
import sys
import re
from skiplist import *

with open('testfile.txt', 'r') as thefile:
    ops, data = thefile.readlines()
    ops = ops.strip('\n')
    data = data.strip('\n')
    bracks = re.compile('(\[|\]|\")')
    ops = re.sub(bracks, '', ops)
    data = re.sub(bracks, '', data)
    print(ops)
    print(data)
    ops = ops.split(',')
    data = data.split(',')
    ops = list(map(lambda x: x.strip('"'), ops))
    data = list(map(lambda x: x.strip('[]'), data))

s = None
for op, item in zip(ops, data):
    if op == 'Skiplist':
        s = Skiplist()
    elif op == 'add':
        s.add(int(item))
        s.printList(backwalk=True)
    elif op == 'search':
        if s.search(int(item)) == True:
            print('Found {}'.format(item))
        else:
            print('Did not find {}'.format(item))
    elif op == 'erase':
        s.erase(int(item))
    else:
        print('There was an error, woopsies.')
s.printList(backwalk=True)
