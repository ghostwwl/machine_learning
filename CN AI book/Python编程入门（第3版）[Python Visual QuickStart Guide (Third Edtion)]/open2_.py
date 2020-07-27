def open2_(fname):

    f = open('grades.dat', 'rb')

    for line in f:
        print(line)
    f.close()
