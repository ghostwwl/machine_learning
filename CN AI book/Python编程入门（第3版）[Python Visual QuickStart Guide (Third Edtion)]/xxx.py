def main():
    color = {'red':1, 'blue':2, 'gress':3, 'orange':4}
    k = color.keys()
    for i in k: print(i)

    color.pop('red')
    color
    print('\n')
    for i in k: print(i)
