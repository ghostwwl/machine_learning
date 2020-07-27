def insert_line(title, fname = 'test.txt'):
    f = open(fname, 'r+')
    tmp = f.read()
    tmp = title + '\n\n' + tmp

    f.seek(0)
    f.write(tmp)

    f.close()
