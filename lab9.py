
# lab9.py
from flask import Blueprint, render_template, request, redirect, url_for, session

# Указываем правильный путь к шаблонам
lab9 = Blueprint('lab9', __name__, template_folder='templates/lab9')

@lab9.route('/lab9/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем, отправлено ли имя пользователя
        if 'name' in request.form and request.form['name'].strip():
            session['name'] = request.form['name'].strip()  # Сохраняем имя в сессии
            return redirect(url_for('lab9.age'))  # Переход на страницу ввода возраста
        else:
            # Если имя не введено, отображаем ошибку
            return render_template('index1.html', error="Введите ваше имя!")
    return render_template('index1.html', last_image=session.get('last_image'))

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        try:
            # Проверяем, что возраст введен корректно
            session['age'] = int(request.form['age'])
            return redirect(url_for('lab9.gender'))
        except ValueError:
            # Обрабатываем случай некорректного ввода
            return render_template('age.html', error="Введите корректный возраст!")
    return render_template('age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        # Сохраняем пол в сессии
        session['gender'] = request.form['gender']
        return redirect(url_for('lab9.preferences'))
    return render_template('gender.html')

@lab9.route('/lab9/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        # Сохраняем предпочтения в сессии
        session['preferences'] = request.form['preferences']
        return redirect(url_for('lab9.final'))
    return render_template('preferences.html')

@lab9.route('/lab9/final', methods=['GET'])
def final():
    # Получаем данные из сессии
    name = session.get('name', 'Гость')
    age = session.get('age', 0)
    gender = session.get('gender', 'мужчина')
    preferences = session.get('preferences', 'сладкое')

    # Логика для определения поздравления и изображения
    message = ""
    image = ""

    if 5 <= age <= 15:
        if gender == "женщина" and preferences == "сладкое":
            message = f"Милая {name}, пусть этот год принесет много сладостей и радости! Вот тебе подарок!"
            image = url_for('static', filename='lab9/image1.jpg')
        elif gender == "мужчина" and preferences == "сладкое":
            message = f"Дорогой {name}, пусть этот год будет сладким и веселым! Вот твой подарок!"
            image = url_for('static', filename='lab9/image2.jpg')
        else:
            message = f"Маленький {name}, пусть этот год будет полон чудес!"
            image = url_for('static', filename='lab9/image_default_kid.jpg')

    elif 15 < age <= 20:
        if gender == "мужчина":
            if preferences == "сладкое":
                message = f"Дорогой {name}, наслаждайся сладостями этого года! Вот твой подарок!"
                image = url_for('static', filename='lab9/image4.jpg')
            elif preferences == "красивое":
                message = f"{name}, желаем тебе новых достижений и успехов в этом году! Вот твой подарок!"
                image = url_for('static', filename='lab9/image3.jpg')
        elif gender == "женщина":
            if preferences == "сладкое":
                message = f"Прекрасная {name}, пусть этот год будет таким же сладким, как этот подарок!"
                image = url_for('static', filename='lab9/image5.jpg')
            elif preferences == "красивое":
                message = f"Милая {name}, пусть этот год принесет тебе много красоты и радости! Вот твой подарок!"
                image = url_for('static', filename='lab9/image6.jpg')

    elif 20 < age <= 40:
        if gender == "мужчина" and preferences == "сладкое":
            message = f"{name}, пусть этот год принесет тебе силы и сладких моментов! Вот твой подарок!"
            image = url_for('static', filename='lab9/image7.jpg')
        elif gender == "женщина" and preferences == "красивое":
            message = f"{name}, пусть этот год будет таким же прекрасным, как этот подарок!"
            image = url_for('static', filename='lab9/image8.jpg')
        else:
            message = f"Дорогой {name}, пусть этот год будет ярким и насыщенным!"
            image = url_for('static', filename='lab9/image_default_adult.jpg')

    elif 40 < age <= 100:
        if gender == "мужчина":
            if preferences == "сладкое":
                message = f"Уважаемый {name}, пусть этот год принесет вам сладкие радости и успех! Вот ваш подарок!"
                image = url_for('static', filename='lab9/image9.jpg')
            elif preferences == "красивое":
                message = f"Дорогой {name}, пусть этот год будет полон красоты и гармонии! Вот ваш подарок!"
                image = url_for('static', filename='lab9/image10.jpg')
        elif gender == "женщина":
            if preferences == "сладкое":
                message = f"Прекрасная {name}, пусть этот год будет сладким и незабываемым! Вот ваш подарок!"
                image = url_for('static', filename='lab9/image11.jpg')
            elif preferences == "красивое":
                message = f"Уважаемая {name}, пусть этот год подарит вам красоту и счастье! Вот ваш подарок!"
                image = url_for('static', filename='lab9/image12.jpg')

    else:
        message = f"Уважаемый {name}, поздравляем с Новым годом! Желаем вам счастья и удачи!"
        image = url_for('static', filename='lab9/image_default.jpg')

    # Сохраняем путь к изображению в сессии для отображения на главной странице
    session['last_image'] = image

    return render_template('final.html', name=name, age=age, gender=gender, preferences=preferences, message=message, image=image)
