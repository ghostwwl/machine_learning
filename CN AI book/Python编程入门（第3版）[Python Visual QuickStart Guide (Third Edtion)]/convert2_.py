def convert_to_int2(s, base):
    try:
        return int(s, base)
    
    except ValueError:
        return ('value error')
    except TypeError:
        return ('type error')
