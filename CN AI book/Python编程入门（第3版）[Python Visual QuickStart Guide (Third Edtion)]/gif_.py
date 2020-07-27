def is_gif(fname):
    f = open(fname, 'br')
    first4 = tuple(f.read(4))
    return first4 == (0x47, 0x49, 0x46, 0x48)
