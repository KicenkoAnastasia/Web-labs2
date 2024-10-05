from flask import Flask, url_for, redirect, make_response, render_template

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
            <ul>
                <li><a href="/lab2">Вторая лабораторная</a></li>
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

# 402 Payment Required 
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

# 418 I'm a teapot
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

    #8
    
    # Маршрут, который вызывает ошибку
@app.route('/error')
def trigger_error():
    result = 1 / 0  
    return f"Результат: {result}"

# Перехватчик ошибки 500 
@app.errorhandler(500)
def internal_server_error(error):
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 500 - Внутренняя ошибка сервера</title>
        </head>
        <body>
            <h1>Ошибка 500</h1>
            <p>Произошла внутренняя ошибка сервера. Пожалуйста, попробуйте позже.</p>
            <p>Если ошибка повторяется, обратитесь в службу поддержки.</p>
        </body>
    </html>
    ''', 500

#9
@app.route('/homa')
def homa():
   
    path1 = url_for("static", filename="hom1.jpg")
    path2 = url_for("static", filename="hom2.jpg")
    css_path = url_for("static", filename="9.css")
    
   
    content = '''
    <!doctype html>
    <html>
        <head><title>О хомяке</title>
        
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
        <link href="https://fonts.googleapis.com/css2?family=TT+Norms+Tochka+Extended+DemiBold&display=swap" rel="stylesheet">
        </head>
        <body>
        <header>
                <h1>Мемы с хомяком</h1>
            </header>
            <div>
                <div>
                    <h1> Что означает мем с хомяком</h1>
                    <p>Пользователи придумали два варианта шаблона: в первом мы весь ролик смотрим на хомяка, которого сопровождает описание 
                    грустной ситуации. А во втором — можем переключить две картинки: с событием и животным, которое показывает своим 
                    видом отношение к ситуации</p>
                </div>
                <div>
                    <h2> Какие есть мемы с хомяком </h2>
                    <img src="''' + path1 + '''" >
                    <p>Мем используют, чтобы проиллюстрировать ситуации, когда у человека наворачиваются слезы на глаза. Это может быть как печаль, потому что случилось что-то плохое или сбивающее с толку, так и просто 
                    блеск в глазах — например, когда человек хочет что-то получить и для этого старается выглядеть более милым и трогательным.Когда просто 
                    блестят глаза. Грустный хомяк подходит, чтобы показать эмоции, как у кота из Шрека. Когда ты такой милый, но все равно или чем-то провинился,
                    или что-то сделал не так, как все ожидают.</p>
                    <p> Когда случилось что-то плохое. Ситуации могут быть разные — от легкой неловкости до реальной проблемы. В таком случае хомяк 
                    плачет из-за настоящей печали.При этом страдания хомяка могут быть преувеличенными или ироничными.</p>
                    <img src="''' + path2 + '''" >
                </div>
            </div>
        </body>
    </html>
    '''
    
    # Создание ответа с заголовками
    response = make_response(content)
    response.headers['Content-Language'] = 'ru' 
    response.headers['Custom-Header-1'] = 'CustomValue1'  # заголовок 1
    response.headers['Custom-Header-1'] = 'CustomValue2'  # заголовок 2
    
    return response



#ЛАБОРАТОРНАЯ №2---------------------------------------------------------------------------------------------------
@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка', 'пион']

# 1. Добавление цветка с проверкой имени
@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if not name:
        return "вы не задали имя цветка", 400
    flower_list.append(name)
    return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка:  {name} </p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
            <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
            </body>
        </html>
        '''

# 2. Вывод всех цветов и их количества
@app.route('/lab2/flowers')
def all_flowers():
    return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Все цветы</h1>
            <p>Количество цветов: {len(flower_list)}</p>
            <ul>
                {''.join([f'<li>{flower}</li>' for flower in flower_list])}
            </ul>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
            </body>
        </html>
        '''

# 3. Улучшенный вывод конкретного цветка (название функции изменено)
@app.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list):
        return '''
            <!doctype html>
            <html>
                <body>
                <h1>Такого цветка нет</h1>
                <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
                </body>
            </html>
            ''', 404
    else:
        return f'''
            <!doctype html>
            <html>
                <body>
                <h1>Цветок: {flower_list[flower_id]}</h1>
                <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
                </body>
            </html>
            '''

# 4. Очистка списка цветов
@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
        <!doctype html>
        <html>
            <body>
            <h1>Список цветов очищен</h1>
            <p>Все цветы были удалены.</p>
            <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
            </body>
        </html>
        '''


@app.route('/lab2/example')
def example():
    name = 'Киценко А.В'  # Имя студента
    lab_num = None        # Номер лабораторной
    group = None          # Группа
    course_number = 3     # Курс

    fruits = [
        {'name':'яблоки','price': 100 }, 
        {'name':'груши','price': 120}, 
        {'name':'апельсины','price': 80}, 
        {'name':'мандарины','price': 95}, 
        {'name':'манго','price': 312}
        ]
    
    # Передаем переменные в шаблон
    return render_template('example.html', name=name, lab_num=lab_num, group=group, course_number=course_number, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "Неверующие в <b>туриста</b> такие типа: <u>наверное</u> большинство людей умирают по <i>причине</i> болезни или старости"
    return render_template('filter.html', phrase=phrase)


# 2- самостоятельное задание
@app.route('/lab2/calc/')
def default_calc():
    # Перенаправляем на /lab2/calc/1/1
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def redirect_to_one(a):
    # Перенаправляем на /lab2/calc/a/1
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    # Выполняем математические операции
    results = {
        "sum": a + b,
        "difference": a - b,
        "product": a * b,
        "division": a / b if b != 0 else "деление на ноль",
        "power": a ** b
    }

    return f'''
        <!doctype html>
        <html>
            <head>
                <title>Результаты расчетов</title>
            </head>
            <body>
                <h1>Расчёт с параметрами:</h1>
                <ul>
                    <li>{a} + {b} = {results["sum"]}</li>
                    <li>{a} - {b} = {results["difference"]}</li>
                    <li>{a} x {b} = {results["product"]}</li>
                    <li>{a} / {b} = {results["division"]}</li>
                    <li>{a}^{b} = {results["power"]}</li>
                </ul>
                <p><a href="/lab2/calc">Вернуться к расчету</a></p>
            </body>
        </html>
    '''

#3-самостоятельное задание

books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Классическая литература", "pages": 671},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Исторический роман", "pages": 1225},
    {"author": "Джон Толкин", "title": "Властелин колец", "genre": "Фэнтези", "pages": 1178},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 256},
    {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Роман", "pages": 336},
    {"author": "Джордж Мартин", "title": "Игра престолов", "genre": "Фэнтези", "pages": 694},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Мистика", "pages": 480},
    {"author": "Даниэль Дефо", "title": "Робинзон Крузо", "genre": "Приключения", "pages": 320}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)


# 4- кошки - фото
# Список пород кошек
cat_breeds = [
    {
        "name": "Персидская кошка",
        "image": "persian.jpg",
        "description": "Персидские кошки известны своей длинной шерстью и спокойным характером."
    },
    {
        "name": "Сиамская кошка",
        "image": "siamese.jpg",
        "description": "Сиамские кошки выделяются своим стройным телом и ярко-голубыми глазами."
    },
    {
        "name": "Мейн-кун",
        "image": "maine_coon.jpg",
        "description": "Мейн-кун — одна из самых крупных пород кошек с дружелюбным нравом."
    },
    {
        "name": "Бенгальская кошка",
        "image": "bengal.jpg",
        "description": "Бенгальские кошки известны своим леопардовым рисунком и активностью."
    },
    {
        "name": "Обычный рыжий котёнок",
        "image": "turist.jpg",
        "description": "Поздравляем, вам попался обычный рыжий котёнок"
    }
]


@app.route('/cats')
def show_cats():
    return render_template('cats.html', cat_breeds=cat_breeds)


@app.route('/')
def home_page(): 
    return render_template('index.html')