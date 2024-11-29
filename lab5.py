# lab5.py
from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

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
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

# Функция для закрытия соединения с базой данных
def db_close(conn, cur):
    try:
        if conn:
            conn.commit()
    except psycopg2.InterfaceError:
        pass
    finally:
        if cur:
            cur.close()
        if conn:
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
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    finally:
        db_close(conn, cur)

    return redirect(url_for('lab5.login'))

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
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,)) #проверка результатов
        user = cur.fetchone()

        if not user or not check_password_hash(user['password'], password):
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        session['login'] = login
    finally:
        db_close(conn, cur)

    return redirect(url_for('lab5.lab'))

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None) #удаляет из сессии запись о текущем пользователе (если она есть). 
    return redirect(url_for('lab5.lab'))

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            return render_template('lab5/create_article.html', error="Название и текст статьи не могут быть пустыми.")

        conn, cur = db_connect()
        try:
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
            user = cur.fetchone()
            if not user:
                return redirect(url_for('lab5.login'))

            login_id = user["id"]
            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", #запрос к базе данных
                        (login_id, title, article_text))
        finally:
            db_close(conn, cur)

        return redirect(url_for('lab5.list_articles'))

    return render_template('lab5/create_article.html')

@lab5.route('/lab5/list')
def list_articles():
    conn, cur = db_connect()
    try:
        cur.execute("""
            SELECT * FROM articles 
            ORDER BY is_favorite DESC, id DESC;
        """)
        articles = cur.fetchall()
    finally:
        db_close(conn, cur)

    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        article = cur.fetchone()

        if not article:
            return redirect(url_for('lab5.list_articles'))

        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if article['user_id'] != user['id']:
            return redirect(url_for('lab5.list_articles'))

        cur.execute("DELETE FROM articles WHERE id = %s;", (article_id,))
    finally:
        db_close(conn, cur)

    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        article = cur.fetchone()

        if not article:
            return redirect(url_for('lab5.list_articles'))

        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if article['user_id'] != user['id']:
            return redirect(url_for('lab5.list_articles'))

        if request.method == 'POST':
            title = request.form.get('title')
            article_text = request.form.get('article_text')

            if not title or not article_text:
                return render_template('lab5/edit_article.html', article=article, error="Название и текст статьи не могут быть пустыми.")

            cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s;",
                        (title, article_text, article_id))
            return redirect(url_for('lab5.list_articles'))

        return render_template('lab5/edit_article.html', article=article)
    finally:
        db_close(conn, cur)

@lab5.route('/lab5/toggle_favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    try:
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()

        if not user:
            return redirect(url_for('lab5.login'))

        cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        article = cur.fetchone()

        if not article or article['user_id'] != user['id']:
            return redirect(url_for('lab5.list_articles'))

        new_favorite_status = not article['is_favorite']
        cur.execute("UPDATE articles SET is_favorite = %s WHERE id = %s;", (new_favorite_status, article_id))
    finally:
        db_close(conn, cur)

    return redirect(url_for('lab5.list_articles'))


@lab5.route('/lab5/users')
def list_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    conn, cur = db_connect()
# список логинов всех пользователей
    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)

    return render_template('/lab5/users.html', users=users)