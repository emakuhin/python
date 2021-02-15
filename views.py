from functions import render
def index(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)
def about(request):
    names = request.get('name', None)
    return '200 OK', render('about.html', names=names)
