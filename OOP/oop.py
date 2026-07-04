"""OOP concepts
1. Abstraction
2. Encapsulation
3. Inheritance
4. Polymorphism
     """

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def walk(self):
        pass

class Goat(Animal):
    def make_sound(self):
        print("bleats")  


class Sheep(Animal):
    def make_sound(self):
        print("mee mee")  


# goat = Goat()
# goat.walk()

# animal = Animal()


class Student:
    def __init__(self, name, age):
        self.name = name       #public attribute
        self.__age = age    #private attribute  


fake_student = Student("Qaanitat", 12)
print(fake_student.name)
print(fake_student.__age)