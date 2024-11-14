from flask import Blueprint, render_template, request, redirect, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from flask import current_app

lab5 = Blueprint('lab5', __name__)


# Функция для подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kicenko_anastasia_knowledge_base',
            user='kicenko_anastasia_knowledge_base',
            password='123',
            options="-c client_encoding=UTF8"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(_file_))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

# Функция для закрытия соединения с базой данных
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    try:
        # Проверка, существует ли пользователь
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        # Хеширование пароля и создание пользователя
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    finally:
        db_close(conn, cur)

    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()
    try:
        # Проверка наличия пользователя
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()
        
        if not user or not check_password_hash(user['password'], password):
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        session['login'] = login
    finally:
        db_close(conn, cur)

    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))

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
    try:
        # Получение ID пользователя
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        if not user:
            return redirect('/lab5/login')

        login_id = user["id"]
        # Вставка новой статьи
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                    (login_id, title, article_text))
    finally:
        db_close(conn, cur)

    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    try:
        # Получение ID пользователя
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        if not user:
            return redirect('/lab5/login')

        login_id = user["id"]
        # Выборка всех статей пользователя
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id,))
        articles = cur.fetchall()
    finally:
        db_close(conn, cur)

    return render_template('/lab5/articles.html', articles=articles)