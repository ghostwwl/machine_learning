def eat_vowels(s):
    """ Removes the vowels from s
"""
    return ''.join(c for c in s if c.lower() not in 'aeiou')
