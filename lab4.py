from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('/lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!', x1=x1, x2=x2)
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Ошибка: деление на ноль невозможно!', x1=x1, x2=x2)

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sum.html', error='Оба поля должны быть заполнены!', x1=x1, x2=x2)
    
    x1, x2 = int(x1), int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('/lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/mul.html', error='Оба поля должны быть заполнены!', x1=x1, x2=x2)
    
    x1, x2 = int(x1), int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!', x1=x1, x2=x2)
    
    x1, x2 = int(x1), int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('/lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!', x1=x1, x2=x2)
    
    x1, x2 = int(x1), int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0 в степени 0 неопределено!', x1=x1, x2=x2)
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0
MAX_TREES = 7  

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < MAX_TREES:
        tree_count += 1
    
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов', 'gender': 'M'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'M'},
    {'login': 'michelle', 'password': '789', 'name': 'Мишель Ли', 'gender': 'F'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'login' in session
        return render_template('lab4/login.html', authorized=authorized, login=session.get('login', ''), name=session.get('name', ''))

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login)
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

# самостоятельное задание . 2.Холодильник
@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature'))
            if temperature < -12:
                message = 'Ошибка: слишком низкое значение'
            elif temperature > -1:
                message = 'Ошибка: слишком высокое значение'
            else:
                if -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°С ❄️❄️❄️'
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°С ❄️❄️'
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°С ❄️'
        except (TypeError, ValueError):
            message = 'Ошибка: не задана температура'

    return render_template('lab4/fridge.html', message=message)


# самостоятельное задание . 3. Заказ зерна.
grain_prices = {
    'Ячмень': 12345,
    'Овёс': 8522,
    'Пшеница': 8722,
    'Рожь': 14111
}

@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    message = None
    if request.method == 'POST':
        grain = request.form.get('grain') 
        try:
            weight = float(request.form.get('weight'))
            if weight <= 0:
                message = 'Ошибка: вес должен быть больше 0'
            elif weight > 500:
                message = 'Ошибка: такого объёма нет в наличии'
            else:
                price_per_ton = grain_prices[grain]  
                total_price = price_per_ton * weight
                discount_applied = ''
                if weight > 50:
                    total_price *= 0.9  # Скидка 10% за объём
                    discount_applied = ' Применена скидка 10%.'
                message = f'Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб.{discount_applied}'
        except (TypeError, ValueError):
            message = 'Ошибка: некорректно указан вес'
        except KeyError:
            message = 'Ошибка: не поддерживаемое зерно'

    return render_template('lab4/order_grain.html', message=message)


#доп. задание

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')

        if not login or not password or not name:
            return render_template('lab4/register.html', error='Все поля должны быть заполнены')

        for user in users:
            if user['login'] == login:
                return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')

        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        return redirect('/lab4/login')

    return render_template('lab4/register.html')


@lab4.route('/lab4/users', methods=['GET'])
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')  # Перенаправление на страницу логина для неавторизованных пользователей
    
    return render_template('lab4/users.html', users=users)


@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')  # Перенаправление, если пользователь не авторизован
    
    user_login = session['login']
    global users
    users = [user for user in users if user['login'] != user_login]
    
    # Очистка сессии и перенаправление на страницу входа после удаления
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')  # Перенаправление для неавторизованных
    
    user_login = session['login']
    user = next((u for u in users if u['login'] == user_login), None)
    
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')
        
        if user and new_name and new_password:
            user['name'] = new_name
            user['password'] = new_password
            session['name'] = new_name  # Обновление сессии с новым именем
            return redirect('/lab4/users')

    return render_template('lab4/edit_user.html', user=user)