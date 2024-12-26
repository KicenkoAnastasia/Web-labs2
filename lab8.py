from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from db.models import Users, Articles
from db import db

# Создаем Blueprint для лабораторной работы
lab8 = Blueprint('lab8', __name__)

# Главная страница
@lab8.route('/lab8/')
def lab():
    # Отображаем главную страницу. Если пользователь авторизован, передаем его логин в шаблон.
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else None)

# Регистрация пользователя
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    # Если запрос GET, показываем страницу регистрации
    if request.method == 'GET':
        return render_template('lab8/register.html')

    # Получаем данные из формы регистрации
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form or not password_form:
        flash('Логин и пароль не должны быть пустыми!', 'error')
        return redirect(url_for('lab8.register'))

    # Проверяем, существует ли уже пользователь с таким логином
    if Users.query.filter_by(login=login_form).first():
        flash('Такой пользователь уже существует!', 'error')
        return redirect(url_for('lab8.register'))

    # Хешируем пароль перед сохранением
    password_hash = generate_password_hash(password_form)
    
    # Создаем нового пользователя и сохраняем его в базе данных
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Выполняем автоматический вход после регистрации
    login_user(new_user)
    flash('Регистрация успешна! Вы вошли в систему.', 'success')
    return redirect(url_for('lab8.lab'))

# Авторизация пользователя
@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    # Если запрос GET, показываем страницу авторизации
    if request.method == 'GET':
        return render_template('lab8/login.html')

    # Получаем данные из формы авторизации
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = 'remember' in request.form  # Флаг для запоминания пользователя

    # Ищем пользователя по введенному логину
    user = Users.query.filter_by(login=login_form).first()

    # Проверка корректности введенных данных (логин и пароль)
    if not user or not check_password_hash(user.password, password_form):
        flash('Неверный логин или пароль!', 'error')
        return redirect(url_for('lab8.login'))

    # Авторизуем пользователя, если данные верны
    login_user(user, remember=remember)
    flash('Вы успешно вошли в систему!', 'success')
    return redirect(url_for('lab8.lab'))

# Выход пользователя
@lab8.route('/lab8/logout/')
@login_required  # Только для авторизованных пользователей
def logout():
    # Выполняем выход пользователя
    logout_user()
    flash('Вы успешно вышли из системы!', 'success')
    return redirect(url_for('lab8.login'))

# Страница статей с поиском
@lab8.route('/lab8/articles/', methods=['GET'])
def articles():
    # Получаем параметр поиска из строки запроса, если он есть
    search_query = request.args.get('search', '').strip()

    # Если пользователь не авторизован, показываем только публичные статьи
    if not current_user.is_authenticated:
        articles_list = Articles.query.filter_by(is_public=True)
    else:
        # Для авторизованных пользователей показываем их собственные статьи и публичные статьи других пользователей
        articles_list = Articles.query.filter(
            (Articles.login_id == current_user.id) | (Articles.is_public == True)
        )

    # Если есть строка поиска, фильтруем статьи по заголовку или тексту
    if search_query:
        articles_list = articles_list.filter(
            Articles.title.ilike(f'%{search_query}%') |  # Поиск по заголовку
            Articles.article_text.ilike(f'%{search_query}%')  # Поиск по тексту статьи
        )

    articles_list = articles_list.all()  # Получаем все статьи после фильтрации

    # Отправляем данные в шаблон
    return render_template(
        'lab8/articles.html',
        articles=articles_list,
        search_query=search_query,
        login=current_user.login if current_user.is_authenticated else None
    )

# Создание новой статьи
@lab8.route('/lab8/create_article/', methods=['GET', 'POST'])
@login_required  # Только для авторизованных пользователей
def create_article():
    # Если запрос GET, показываем форму для создания статьи
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # Проверяем, указана ли публичность

    # Проверка на пустые поля
    if not title or not article_text:
        flash('Заголовок и текст статьи не должны быть пустыми!', 'error')
        return redirect(url_for('lab8.create_article'))

    # Создаем новый объект статьи и сохраняем его в базе данных
    new_article = Articles(
        login_id=current_user.id,  # Привязываем статью к текущему пользователю
        title=title,
        article_text=article_text,
        is_public=is_public,
        likes=0  # Изначально у статьи нет лайков
    )
    db.session.add(new_article)
    db.session.commit()

    flash('Статья успешно создана!', 'success')
    return redirect(url_for('lab8.articles'))

# Редактирование статьи
@lab8.route('/lab8/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required  # Только для авторизованных пользователей
def edit_article(article_id):
    # Ищем статью по ID и проверяем, что она принадлежит текущему пользователю
    article = Articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        flash('Статья не найдена!', 'error')
        return redirect(url_for('lab8.articles'))

    # Если запрос GET, показываем форму для редактирования статьи
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    # Обновляем данные статьи
    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')
    article.is_public = request.form.get('is_public') == 'on'  # Обновляем публичность статьи

    db.session.commit()  # Сохраняем изменения
    flash('Статья успешно обновлена!', 'success')
    return redirect(url_for('lab8.articles'))

# Удаление статьи
@lab8.route('/lab8/delete_article/<int:article_id>', methods=['POST'])
@login_required  # Только для авторизованных пользователей
def delete_article(article_id):
    # Ищем статью по ID и проверяем, что она принадлежит текущему пользователю
    article = Articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    if not article:
        flash('Статья не найдена!', 'error')
        return redirect(url_for('lab8.articles'))

    db.session.delete(article)  # Удаляем статью из базы данных
    db.session.commit()  # Сохраняем изменения
    flash('Статья успешно удалена!', 'success')
    return redirect(url_for('lab8.articles'))

# Просмотр публичных статей для неавторизованных пользователей
@lab8.route('/lab8/public_articles/', methods=['GET'])
def public_articles():
    # Получаем параметр поиска из строки запроса, если он есть
    search_query = request.args.get('search', '').strip()

    # Показываем только публичные статьи
    articles_list = Articles.query.filter_by(is_public=True)

    # Если есть строка поиска, фильтруем статьи по заголовку или тексту
    if search_query:
        articles_list = articles_list.filter(
            Articles.title.ilike(f'%{search_query}%') |  # Поиск по заголовку
            Articles.article_text.ilike(f'%{search_query}%')  # Поиск по тексту статьи
        )

    articles_list = articles_list.all()  # Получаем все публичные статьи после фильтрации

    return render_template('lab8/public_articles.html', articles=articles_list, search_query=search_query)
