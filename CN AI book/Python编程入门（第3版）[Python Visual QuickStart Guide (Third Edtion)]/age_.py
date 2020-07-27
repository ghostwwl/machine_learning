class Person:
    def __init__(self, name = '', age = 0):
        self._name = name
        self._age = age

    @property
    def age(self):
        return self._age

    def set_age(self):
        if 0 < age <= 150:
            self._age = age

    def display(self):
        print(self)

    def __str__(self):
        return "Person('%s', %s)" % self._name, self._age

    def __repr__(self):
        return str(self)

    @age.setter
    def age(self, age):
        if 0 < age <= 150:
            self._age = age
