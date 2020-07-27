from player import*
from game import*

import random

class Human(Player):

    def __repr__(self):
        return 'Human(%s)' % str(self)

    def get_move(self):
        while True:
            try:
                #n = int(input('%s move (1-10):' % self.get_name()))
                n = int(input('%s move (1-10): '% self.get_name()))
                if 1 <= n <= 10:
                    print('Yes')
                    return n
                else:
                    print('Oops!')
            except:
                print('Oops!')


class Computer(Player):

    def __repr__(self):
        return 'Computer(%s)' % str(self)

    def get_move(self):
        return random.randint(1, 10)
