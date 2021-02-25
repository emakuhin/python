from core import Application
import views
from wsgiref.simple_server import make_server




urlpatterns = {
   '/category/': views.category_list,
    '/course/': views.courses_list,
    '/create_course/': views.create_course,
    '/create_category/': views.create_category
    }

def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'
def names_controller(request):
    request['name'] = ['alex', 'mak', 'sergei', 'Tim']


front_controllers = [
    secret_controller,
    names_controller
]



application = Application(urlpatterns, front_controllers)


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()