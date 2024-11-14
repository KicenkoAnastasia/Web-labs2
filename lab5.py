from flask import Blueprint, render_template, request, redirect, session, url_for
lab5 = Blueprint('lab5', __name__)

import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kicenko_anastasia_knowledge_base',
        user='kicenko_anastasia_knowledge_base',
        password='123',
        options="-c client_encoding=UTF8"  # Принудительно устанавливаем кодировку UTF-8 для соединения
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    

    conn, cur = db_connect()

    cur.execute(f"SELECT login FROM users WHERE login = '{login}';")
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    cur.execute(f"INSERT INTO users (login,password) VALUES ('{login}', '{password_hash}');")

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):  # Проверка на пустые поля
        return render_template('lab5/login.html', error="Заполните поля")

    # Подключение к базе данных
    conn, cur = db_connect()

    #запрос
    cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    # Проверка пароля
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', 
                               error='Логин и/или пароль неверны')


    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)  # Удаляем логин пользователя из сессии
    return redirect(url_for('lab5.lab'))  # Перенаправляем на главную страницу
    

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    # Добавлена запятая перед кортежем (login,)
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    # Исправлено: используется параметризованный запрос для вставки данных
    cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                (login_id, title, article_text))

    # Закрытие соединения
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Get the user's ID based on their login
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    # Select articles where the user_id matches login_id
    cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id,))
    articles = cur.fetchall()

    # Close the database connection
    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)