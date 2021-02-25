from functions import render
from models import TrainingSite
from core import Application
from models import Logger

logger = Logger('main')
site = TrainingSite()
cousers=['Java', 'Python']
def index(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    courses = ['Java', 'Python']
    return '200 OK', render('index.html', secret=secret, courses=courses)
def teachers(request):
    names = request.get('name', None)
    return '200 OK', render('teachers.html', names=names)



def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        name = Application.decode_value(name)
        if not site.find_category(name):
            new_category = site.create_category(name, name)
            site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        for cat in categories:
            print(cat.name)
        return '200 OK', render('create_category.html', categories=categories)

def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = Application.decode_value(data['name'])
        category = Application.decode_value(data.get('category'))
        print('Пришол запрос', category)
        # print(category_id)
        if category:
            course = site.create_course(name, site.find_category(category))
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)

def courses_list(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', courses=site.courses)

def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', items=site.categories)
