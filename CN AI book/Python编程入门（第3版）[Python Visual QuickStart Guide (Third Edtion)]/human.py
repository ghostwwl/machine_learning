from player import *


class Human(Player):
    def __repr__(self):
        return 'Human(%s)' % str(self)

class Computer(Player):
    def __repr__(self):
        return "Computer(%s)" % str(self)
