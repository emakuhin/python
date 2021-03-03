from core import Application
from functions import render
from wsgiref.simple_server import make_server
from models import Logger, TrainingSite, debug, EmailNotifier, SmsNotifier, BaseSerializer



logger = Logger('main')
site = TrainingSite()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()




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
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
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

@application.add_route('/create_student/')
def create_student(request):
    if request['method'] == 'POST':
        data = request['data']
        name = Application.decode_value(data['name'])
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
    return '200 OK', render('create_student.html')

@application.add_route('/students/')
def student_list(request):
    return '200 OK', render('student_list.html', students=site.students)


@application.add_route('/add_student/')
@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        student_name = data['student']
        student = site.get_student(student_name)
        course_name = data.get('courses')
        course = site.get_course(course_name)
        course.add_student(student)
        print(f'Пришол запрос от {student} записаться на курс {course}')
        courses = site.courses
        students = site.students
        return '200 OK', render('create_course.html', courses=courses, students=students)
    else:
        courses = site.courses
        students = site.students
        return '200 OK', render('add_student.html', courses=courses, students=students)

@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()