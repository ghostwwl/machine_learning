class Player:
    
    def __init__(self, name):
        self._name = name
        self._score = 0
    def reset_score(self):
        self._score = 0
    def incr_score(self):
        self._score += 1
    def get_name(self):
        return self._name
    def __str__(self):
        return "name = '%s', score = %s" % (self._name, self._score)
    def __repr__(self):
        return 'Player %s' % str(self)
