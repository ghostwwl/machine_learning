def invert(x):
    try:
        return 1/x
    except ZeroDivisionError:
        return 'error'
    finally:
        print('invert(%s) done' %x)
