import os

def list_cwd():
    """ Return current working directory
"""
    return os.listdir(os.getcwd())

def files_cwd():
    """ Return files
"""
    return [p for p in list_cwd() if os.path.isfile(p)]

def folders_cwd():
    """ Return folders
"""
    return [p for p in list_cwd() if os.path.isdir(p)]

def list_py(path = None):
    """ Return the files if it's endswith '.py'
"""
    if(path == None):
        path =os.getcwd()
        return [fname for fname in os.listdir(path)
        if os.path.isfile(fname)
        if fname.endswith('.py')]
    
def size_in_bytes(fname):
    """ Return the size of a file
"""
    return os.stat(fname).st_size

def cwd_size_in_bytes():
    """ Return the total sizes of files
"""
    total = 0
    for name in files_cwd():
        total += size_in_bytes(name)
    return total
