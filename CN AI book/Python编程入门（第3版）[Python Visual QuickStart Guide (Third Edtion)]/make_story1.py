import os

def make_story2():
    if os.path.isfile('test.txt'):
        print('test.txt already exists')
    else:
        f = open('test.txt', 'w')
        f.write('I love, \n')
        f.write('you.\n')
