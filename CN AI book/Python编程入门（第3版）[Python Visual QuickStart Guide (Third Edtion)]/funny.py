import re
def is_funny(s):
    return re.match('(ha)+!+', s) != None

