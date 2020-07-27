def add_to_test(line, fname = 'test.txt'):
    f = open(fname, 'a')
    f.write(line)
