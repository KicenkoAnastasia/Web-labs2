from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from db.models import Users, Articles
from db import db

lab8 = Blueprint('lab8', __name__)

# Главная страница
@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else None)

# Регистрация пользователя
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        flash('Логин и пароль не должны быть пустыми!', 'error')
        return redirect(url_for('lab8.register'))

    if Users.query.filter_by(login=login_form).first():
        flash('Такой пользователь уже существует!', 'error')
        return redirect(url_for('lab8.register'))

    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический вход
    login_user(new_user)
    flash('Регистрация успешна! Вы вошли в систему.', 'success')
    return redirect(url_for('lab8.lab'))

# Авторизация пользователя
@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = 'remember' in request.form  # Запомнить пользователя

    user = Users.query.filter_by(login=login_form).first()

    if not user or not check_password_hash(user.password, password_form):
        flash('Неверный логин или пароль!', 'error')
        return redirect(url_for('lab8.login'))

    login_user(user, remember=remember)  # Используем remember
    flash('Вы успешно вошли в систему!', 'success')
    return redirect(url_for('lab8.lab'))

# Выход пользователя
@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы!', 'success')
    return redirect(url_for('lab8.login'))

# Страница статей
@lab8.route('/lab8/articles/')
@login_required
def articles():
    articles_list = Articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=articles_list, login=current_user.login)

# Создание статьи
@lab8.route('/lab8/create_article/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        flash('Заголовок и текст статьи не должны быть пустыми!', 'error')
        return redirect(url_for('lab8.create_article'))

    new_article = Articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=True,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()

    flash('Статья успешно создана!', 'success')
    return redirect(url_for('lab8.articles'))

# Редактирование статьи
@lab8.route('/lab8/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        flash('Статья не найдена!', 'error')
        return redirect(url_for('lab8.articles'))

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')

    db.session.commit()
    flash('Статья успешно обновлена!', 'success')
    return redirect(url_for('lab8.articles'))

# Удаление статьи
@lab8.route('/lab8/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        flash('Статья не найдена!', 'error')
        return redirect(url_for('lab8.articles'))

    db.session.delete(article)
    db.session.commit()
    flash('Статья успешно удалена!', 'success')
    return redirect(url_for('lab8.articles'))