from singletone import SingletonByName
import time

class TrainingSite:
    def __init__(self):
        self.teachers = ['alex', 'mak', 'sergei', 'Tim']
        self.courses = []
        self.categories = []

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def create_course(name, category):
        return Course(name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def find_category(self, category):
        for item in self.categories:
            print('item', item.category)
            if item.category == category:
                return item
        return False



class Category:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result



class Course:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text)

