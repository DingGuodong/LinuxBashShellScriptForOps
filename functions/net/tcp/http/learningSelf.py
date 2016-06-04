"""
some basic references for using python
"""
import re
import time

foo = 1
show_output = True
if show_output and foo == 1:
    print 'python and %s are number %d ' % ('Django', foo)
text1 = 'hello'
text2 = 'world'
print '%s %s ' % (text1, text2)
print ''.join(['hello', ' ', 'world'])
list1 = ['hello', 'world']
list1.insert(1, ' ')
print list1

tuple1 = ('a', 'b')
for name in tuple1:
    print name

# use time module
print time.ctime()

dict1 = {'a': 1, 'b': 2}
print dict1['a'], dict1['b']

dict2 = {'a': '1', 'b': '2'}
print dict2['a'], dict2['b']
if dict2['a'] == dict1['a']:
    print 1
else:
    print 2

if dict2['a'] == 1:
    print 1
else:
    print 2

if dict2['a'] == '1':
    print 1
elif dict2['a'] == 1:
    print 2
else:
    print 3

data1 = ('a', 'b', 'c')
for i, value in enumerate(data1):
    print i, value

i = 0
while i < 5:
    print i
    i += 1

try:
    f = open('learningSelf.py', 'r')
except IOError as e:
    print e
except (IOError, KeyboardInterrupt) as e:
    print e
finally:
    print 1

# w, if file_exist then purge it first and write.
file1 = open('filename', 'w')
file1.write('hello ')
file1.write('world!')
file1.close()
file1 = open('filename', 'r')
for line in file1:
    print line.rstrip()
file1.close()

# a, append file content
file2 = open('filename', 'a')
file2.write('\n+ hello ')
file2.write('world!')
file2.close()
file3 = open('filename', 'r')
for line in file3:
    print line.rstrip()
file3.close()


def foo(x):
    print x


foo(1)

text3 = "hello world"
obj1 = re.match(r'lo', text3)
if obj1 is not None:
    print obj1.group()
else:
    print 'e'

obj2 = re.search(r'lo', text3)
if obj2 is not None:
    print obj2.group()
else:
    print 'e'
