keep = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'
        , 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', "'", '-'}

def normalize(s):
    """Convert s to a normalized string.
"""
    result = '';

    for c in s.lower():
        if c in keep:
            result += c
    return result
