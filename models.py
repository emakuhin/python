from singletone import SingletonByName
import time
import jsonpickle
from unitofwork import DomainObject

class User:
    def __init__(self, name):
        self.name = name

class Teacher(User):
    pass

class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class TrainingSite:
    def __init__(self):
        self.teachers = ['alex', 'mak', 'sergei', 'Tim']
        self.courses = []
        self.categories = []
        self.students = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item


class Category:

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)

class Observer:

    def update(self, subject):
        pass


class Course(Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class SmsNotifier(Observer):

    def update(self, subject: Course):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject: Course):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))

class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text)

def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG-------->', func.__name__, end - start)
        return result
    return inner




class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    def load(self, data):
        return jsonpickle.loads(data)
