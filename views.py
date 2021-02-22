from functions import render
cousers=['Java', 'Python']
def index(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    courses = ['Java', 'Python']
    return '200 OK', render('index.html', secret=secret, courses=courses)
def teachers(request):
    names = request.get('name', None)
    return '200 OK', render('teachers.html', names=names)
def create_course(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с просьбой создать курс {title} и текстом {text}')
        return '200 OK', render('contact_post.html', title=title, text=text, email=email)
    else:
        return '200 OK', render('contact.html')
