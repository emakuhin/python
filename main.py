from core import Application
from functions import render
from wsgiref.simple_server import make_server
from models import Logger, TrainingSite, debug



logger = Logger('main')
site = TrainingSite()




def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'
def names_controller(request):
    request['name'] = ['alex', 'mak', 'sergei', 'Tim']


front_controllers = [
    secret_controller,
    names_controller
]


urlpatterns = {}

application = Application(urlpatterns, front_controllers)

@application.add_route('/create_category/')
@debug
def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        name = Application.decode_value(name)
        if not site.find_category(name):
            new_category = site.create_category(name, name)
            site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        for cat in categories:
            print(cat.name)
        return '200 OK', render('create_category.html', categories=categories)



@application.add_route('/create_course/')
@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = Application.decode_value(data['name'])
        category = Application.decode_value(data.get('category'))
        print('Пришол запрос', category)
        if category:
            course = site.create_course(name, site.find_category(category))
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)

@application.add_route('/course/')
@debug
def courses_list(request):
    return '200 OK', render('course_list.html', courses=site.courses)

@application.add_route('/category/')
@debug
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', items=site.categories)



with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()