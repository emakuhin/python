from core import Application
import views

urlpatterns = {
    '/': views.index,
    '/about/': views.about
    }

def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'
def names_controller(request):
    request['name'] = ['alex', 'mak', 'sergei']


front_controllers = [
    secret_controller,
    names_controller
]



application = Application(urlpatterns, front_controllers)
