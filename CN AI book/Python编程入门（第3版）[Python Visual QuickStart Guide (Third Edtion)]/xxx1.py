import re

def main():
    color = {'red':1, 'blue':2, 'gress':3, 'orange':4}
    map = color.copy()
    print('color:', color)
    print('map:', map)
    
    lst = []
    k = color.values()
    for i in k:
        print('values:', i, end = ' ')
        if i >= 1:
            lst.append(i)
    print('\nlst:', lst)
    print('\n')

    map.clear()
    color.clear()
####################################################
    
    map = {6:'red', 5:'blue', 4:'gress', 3:'orange', 2:'gresssss!', 1:'gressss!!'}
    color = map.copy()
    print('color:', color)
    print('map:', map)
    
    result = []
    k = map.items()
    for i in k:
        print('items:', i, end = ' ')
        d = re.match('gress', i[1])
        if d:
            result.append(i[1])
    print('\nresult:', result)

    map.clear()
    color.clear()
