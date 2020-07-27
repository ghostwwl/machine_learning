class Person:
    """ class to reperesent a person
"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

#    def display(self):
#       print("Person('%s', %d)" %(self.name, self.age))

    def __str__(self):
        return "Person('%s', %d)" % (self.name, self.age)

#    def display_2(self):
#       print(str(self))

    def __repr__(self):
        return str(self)

    def display(self):
        print(self)

    def set_age(self, age):
        if 0 < age <= 150:
            self.age = age
@property
def age(self):
    """ Return this persons's age.
"""
    return self._age
