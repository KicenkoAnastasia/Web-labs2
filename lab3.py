from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    # Получение значения куки с именем 'name' и 'age'
    name = request.cookies.get('name', 'аноним')  # Значение по умолчанию - 'аноним'
    name_color = request.cookies.get('name_color', 'неизвестный')  # Значение по умолчанию - 'неизвестный'
    age = request.cookies.get('age', 'неизвестный возраст')  # Значение по умолчанию - 'неизвестный возраст'
    
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    # объект ответа
    resp = make_response(redirect('/lab3/'))  
    # Установка куки
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp  

#очистка куки 
@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}

    # Получение значений полей
    user = request.args.get('user', None)
    age = request.args.get('age', None)
    sex = request.args.get('sex', '')

    # Проверка на пустые значения, только если форма отправлена
    if request.args:
        if not user:
            errors['user'] = 'Заполните поле!'
        if not age:
            errors['age'] = 'Заполните поле!'

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order.html')
def order():
    return render_template('/lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black tea':
        price = 80
    else:
        price = 70

    #добавка удорожает цену
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/pay_success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    # параметры из запроса
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    # Устанавливаем куки, если параметры переданы
    resp = make_response(redirect('/lab3/settings')) if color or background_color or font_size or font_style else None

    if color:
        resp.set_cookie('color', color)
    if background_color:
        resp.set_cookie('background_color', background_color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_style:
        resp.set_cookie('font_style', font_style)

    # значения из куки, если параметры не были переданы
    color = color or request.cookies.get('color') or '#000000'
    background_color = background_color or request.cookies.get('background_color') or '#ffffff'
    font_size = font_size or request.cookies.get('font_size') or '16'
    font_style = font_style or request.cookies.get('font_style') or 'normal'

    # Если нет ответа, создаем его для рендеринга шаблона
    if resp is None:
        resp = make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size, font_style=font_style))

    return resp


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect(url_for('lab3.settings')))
    # Удаление всех куков
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp


@lab3.route('/lab3/ticket_form/')
def ticket_form():
    return render_template('lab3/ticket_form.html')

@lab3.route('/lab3/submit_ticket/', methods=['POST'])
def submit_ticket():
    # Получаем данные из формы
    fio = request.form.get('fio')
    shelf = request.form.get('shelf')
    bedding = request.form.get('bedding') == 'on'
    luggage = request.form.get('luggage') == 'on'
    age = int(request.form.get('age'))
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date = request.form.get('date')
    insurance = request.form.get('insurance') == 'on'

    # Проверка возраста
    if age < 1 or age > 120:
        return "Возраст должен быть от 1 до 120 лет", 400

    # Определение стоимости билета
    base_price = 1000 if age >= 18 else 700
    if shelf in ['нижняя', 'нижняя боковая']:
        base_price += 100
    if bedding:
        base_price += 75
    if luggage:
        base_price += 250
    if insurance:
        base_price += 150

    # Создание страницы с билетом
    ticket_info = {
        'fio': fio,
        'shelf': shelf,
        'age': age,
        'departure': departure,
        'destination': destination,
        'date': date,
        'price': base_price,
        'ticket_type': 'Детский билет' if age < 18 else 'Взрослый билет'
    }

    return render_template('lab3/ticket.html', ticket_info=ticket_info)



# Список товаров (смартфоны)
products = [
    {"name": "Смартфон A", "price": 15000, "color": "черный", "brand": "Бренд X"},
    {"name": "Смартфон B", "price": 20000, "color": "белый", "brand": "Бренд Y"},
    {"name": "Смартфон C", "price": 25000, "color": "зеленый", "brand": "Бренд Z"},
    {"name": "Смартфон D", "price": 30000, "color": "синий", "brand": "Бренд W"},
    {"name": "Смартфон E", "price": 35000, "color": "красный", "brand": "Бренд V"},
    {"name": "Смартфон F", "price": 45000, "color": "черный", "brand": "Бренд U"},
    {"name": "Смартфон G", "price": 50000, "color": "белый", "brand": "Бренд T"},
    {"name": "Смартфон H", "price": 60000, "color": "серый", "brand": "Бренд S"},
    {"name": "Смартфон I", "price": 70000, "color": "синий", "brand": "Бренд R"},
    {"name": "Смартфон J", "price": 80000, "color": "зеленый", "brand": "Бренд Q"},
    {"name": "Смартфон K", "price": 90000, "color": "черный", "brand": "Бренд P"},
    {"name": "Смартфон L", "price": 100000, "color": "белый", "brand": "Бренд O"},
    {"name": "Смартфон M", "price": 110000, "color": "красный", "brand": "Бренд N"},
    {"name": "Смартфон N", "price": 120000, "color": "синий", "brand": "Бренд M"},
    {"name": "Смартфон O", "price": 130000, "color": "серый", "brand": "Бренд L"},
    {"name": "Смартфон P", "price": 140000, "color": "черный", "brand": "Бренд K"},
    {"name": "Смартфон Q", "price": 150000, "color": "белый", "brand": "Бренд J"},
    {"name": "Смартфон R", "price": 160000, "color": "зеленый", "brand": "Бренд I"},
    {"name": "Смартфон S", "price": 170000, "color": "красный", "brand": "Бренд H"},
    {"name": "Смартфон T", "price": 180000, "color": "синий", "brand": "Бренд G"},
]

@lab3.route('/lab3/search/', methods=['GET', 'POST'])
def search_form():
    return render_template('lab3/search_form.html')

@lab3.route('/lab3/results/', methods=['POST'])
def search_results():
    min_price = request.form.get('min_price', type=float)
    max_price = request.form.get('max_price', type=float)

    # Фильтрация товаров по цене
    filtered_products = [
        product for product in products
        if min_price <= product['price'] <= max_price
    ]

    return render_template('lab3/search_results.html', products=filtered_products)