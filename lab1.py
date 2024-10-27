from flask import Blueprint, url_for
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
    css_path = url_for("static", filename="lab1/menu.css")
    return '''
        <!doctype html>
        <html>
            <head>
                <title>Лабораторная 1</title>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
            </head>
            <body>
                <header>
                    <h1>НГТУ | ФБ | WEB-программирование | часть 2</h1>
                </header>
                
                <nav class="text">
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </nav>

                <nav>
                   <a href="/">
                        <div class="back"> 
                        на главную
                        </div>
                    </a>
                </nav>

                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/">/ - Главная</a></li>
                    <li><a href="/lab1">/lab1 - Лабораторная 1</a></li>
                    <li><a href="/lab1/web">/lab1/web - Web-сервер на Flask</a></li>
                    <li><a href="/lab1/author">/lab1/author - Страница автора</a></li>
                    <li><a href="/lab1/oak">/lab1/oak - Страница с изображением</a></li>
                    <li><a href="/lab1/counter">/lab1/counter - Счётчик посещений</a></li>
                    <li><a href="/lab1/reset_counter">/lab1/reset_counter - Сброс счётчика</a></li>
                    <li><a href="/400">/400 - код 400 </a></li>
                    <li><a href="/401">/401 - код 401 </a></li>
                    <li><a href="/402">/402 - код 402 </a></li>
                    <li><a href="/403">/403 - код 403 </a></li>
                    <li><a href="/404">/404 - код 404 </a></li>
                    <li><a href="/405">/405 - код 405 </a></li>
                    <li><a href="/homa">/homa - грустный хомяк </a></li>
                </ul>

                <footer>
                    <p>Киценко Анастасия Валерьевна</p>
                    <p>ФБИ-21, Факультет ФБ, 2024 год</p>
                </footer>
            </body>
        </html>
    '''


@lab1.route("/lab1/web")
def web(): 
    return """<!doctype html>
        <html>
           <body>
               <h1>Web-сервер на flask</h1>
           </body>
        </html>""", 200, {
            'X-Server': 'turist', 
            'Content-Type': 'text/plain; charset=utf-8'
            }


@lab1.route("/lab1/author")
def author():
    name = 'Киценко Анастасия Валерьевна'
    group = 'ФБИ-21'
    faculty = 'ФБ'

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
            </body>
        </html>"""


@lab1.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Турист</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''


count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        <p>Сколько раз вы сюда заходили: ''' + str(count) + '''</p>
        <a href="/lab1/reset_counter">Очистить счётчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <p>Счётчик был очищен.</p>
        <a href="/lab1/counter">Вернуться на страницу счётчика</a>
    </body>
</html>
'''


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создан успешно</h1>
        <div><i>Что-то создано...</i></div>
    </body>
</html>
''', 201