from flask import Flask, url_for, redirect
app = Flask (__name__)


@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
        </header>
        
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        
        <footer>
            <p>Киценко Анастасия Валерьевна</p>
            <p>ФБИ-21, Факультет ФБ, 2024 год</p>
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="menu.css")
    
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
                        Назад  
                        </div>
                    </a>
                 </nav>
                <footer>
                    <p>Киценко Анастасия Валерьевна</p>
                    <p>ФБИ-21, Факультет ФБ, 2024 год</p>
                </footer>
            </body>
        </html>
    '''



@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
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

@app.route('/lab1/counter')
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

@app.route('/lab1/reset_counter')
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

if __name__ == '__main__':
    app.run(debug=True)





@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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

# app = Flask(__name__)

# @app.errorhandler(404)
# def not_found(err):
#     return "нет такой страницы", 404




#коды 
# 400 Bad Request
@app.route('/400')
def bad_request():
    return '''
    <!doctype html>
    <html>
        <head><title>400 Bad Request</title></head>
        <body>
            <h1>400 Bad Request</h1>
            <p>Ваш запрос был неверным или неполным.</p>
        </body>
    </html>
    ''', 400

# 401 Unauthorized
@app.route('/401')
def unauthorized():
    return '''
    <!doctype html>
    <html>
        <head><title>401 Unauthorized</title></head>
        <body>
            <h1>401 Unauthorized</h1>
            <p>Доступ запрещён. Необходима авторизация.</p>
        </body>
    </html>
    ''', 401

# 402 Payment Required (зарезервирован для будущего использования)
@app.route('/402')
def payment_required():
    return '''
    <!doctype html>
    <html>
        <head><title>402 Payment Required</title></head>
        <body>
            <h1>402 Payment Required</h1>
            <p>Эта функция требует оплаты.</p>
        </body>
    </html>
    ''', 402

# 403 Forbidden
@app.route('/403')
def forbidden():
    return '''
    <!doctype html>
    <html>
        <head><title>403 Forbidden</title></head>
        <body>
            <h1>403 Forbidden</h1>
            <p>У вас нет прав для доступа к этому ресурсу.</p>
        </body>
    </html>
    ''', 403

# 404 Not Found
@app.route('/404')
def not_found():
    path = url_for("static", filename="KOT2.jpg")
    css_path = url_for("static", filename="404.css")
    return '''
    <!doctype html>
    <html>
        <head>
            <title>404 Method Not Allowed</title>
            <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- Подключение CSS -->
        </head>
        <body>
            <div class="block">
                <div class="per">
                    <h1>AAAAAAA?</h1>
                    <p class="raz"><b>Ошибка 404. Ништяяяк</b></p>
                </div>
                <div class="vtor">
                    <img src="''' + path + '''">
                </div>
            </div>
        </body>
    </html>
    ''', 404

# 405 Method Not Allowed
@app.route('/405')
def method_not_allowed():
    return '''
    <!doctype html>
    <html>
        <head><title>405 Method Not Allowed</title></head>
        <body>
            <h1>405 Method Not Allowed</h1>
            <p>Метод запроса не поддерживается для данного ресурса.</p>
        </body>
    </html>
    ''', 405

# 418 I'm a teapot (шутливый код)
@app.route('/418')
def teapot():
    return '''
    <!doctype html>
    <html>
        <head><title>418 I'm a teapot</title></head>
        <body>
            <h1>418 I'm a teapot</h1>
            <p>Я чайник. Этот сервер не может заварить кофе.</p>
        </body>
    </html>
    ''', 418