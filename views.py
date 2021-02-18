from functions import render
def index(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)
def about(request):
    names = request.get('name', None)
    return '200 OK', render('about.html', names=names)
def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        return '200 OK', render('contact_post.html', title=title, text=text, email=email)
    else:
        return '200 OK', render('contact.html')
