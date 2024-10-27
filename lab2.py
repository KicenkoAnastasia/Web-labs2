from flask import Blueprint, url_for, render_template, redirect,request
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка', 'пион']

# 1. Добавление цветка с проверкой имени
@lab2.route('/lab2/add_flower/', defaults={'name': None})
@lab2.route('/lab2/add_flower/<name>')
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
@lab2.route('/lab2/flowers')
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
@lab2.route('/lab2/flowers/<int:flower_id>')
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
@lab2.route('/lab2/clear_flowers')
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


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab2_home():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "Неверующие в <b>туриста</b> такие типа: <u>наверное</u> большинство людей умирают по <i>причине</i> болезни или старости"
    return render_template('lab2/filter.html', phrase=phrase)


# 2- самостоятельное задание
@lab2.route('/lab2/calc/')
def default_calc():
    # Перенаправляем на /lab2/calc/1/1
    return redirect(url_for('calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def redirect_to_one(a):
    # Перенаправляем на /lab2/calc/a/1
    return redirect(url_for('calc', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/books')
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


@lab2.route('/cats')
def show_cats():
    return render_template('lab2/cats.html', cat_breeds=cat_breeds)


@lab2.route('/')
def home_page(): 
    return render_template('index.html')


# доп.задания
flower_list = [
    {'name': 'роза', 'price': 100},
    {'name': 'тюльпан', 'price': 50},
    {'name': 'незабудка', 'price': 70},
    {'name': 'ромашка', 'price': 30},
    {'name': 'пион', 'price': 120}
]

@lab2.route('/lab2/cvetok/add', methods=['POST'])
def add_cvetok():
    name = request.form.get('name')
    price = request.form.get('price')
    
    if not name or not price:
        return "Необходимо указать название и цену цветка", 400
    
    flower_list.lab2end({'name': name, 'price': int(price)})
    return redirect(url_for('all_cvetki'))


@lab2.route('/lab2/cvetok')
def all_cvetki():
    return render_template('cvetki.html', flowers=flower_list)


@lab2.route('/lab2/cvetok/delete/<int:flower_id>')
def delete_cvetok(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок не найден", 404
    flower_list.pop(flower_id)
    return redirect(url_for('all_cvetki'))


@lab2.route('/lab2/cvetok/clear')
def clear_cvetki():
    flower_list.clear()
    return redirect(url_for('all_cvetki'))

