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