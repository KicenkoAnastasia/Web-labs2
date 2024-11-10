from flask import Blueprint, render_template, request, redirect, session, url_for
lab5 = Blueprint('lab5', __name__)

import psycopg2
from psycopg2.extras import RealDictCursor

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'kicenko_anastasia_knowledge_base',
        user = 'kicenko_anastasia_knowledge_base',
        password ='123'
    )

    cur = conn.cursor(cursor_factory = RealDictCursor)

    cur.execute(f"SELECT login FROM users WHERE login = '{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует")
    
    cur.execute(f"INSERT INTO users (login,password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):  # Проверка на пустые поля
        return render_template('lab5/login.html', error="Заполните поля")

    # Подключаемся к базе данных
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kicenko_anastasia_knowledge_base',
        user='kicenko_anastasia_knowledge_base',
        password='123'
    )

    #получение результатов как словарь
    cur = conn.cursor(cursor_factory=RealDictCursor)

    #запрос
    cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    # Проверяем пароль
    if user['password'] != password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', 
                               error='Логин и/или пароль неверны')


    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)  # Удаляем логин пользователя из сессии
    return redirect(url_for('lab5.lab'))  # Перенаправляем на главную страницу лабораторной