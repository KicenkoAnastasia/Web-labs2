from flask import Blueprint, render_template,url_for
lab3 = Blueprint ('lab3', __name__)


@lab3.route('/lab3/')
def lab3_home():
    css_path = url_for("static", filename="menu.css")
    return '''
        <!doctype html>
        <html>
            <head>
                <title>Лабораторная 3</title>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
            </head>
            <body>
                <header>
                    <h1>НГТУ | ФБ | WEB-программирование | часть 2</h1>
                </header>
                <nav>
                   <a href="/">
                        <div class="back"> 
                        на главную
                        </div>
                    </a>
                </nav>

                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/"> Главная</a></li>
                    <li><a href="/lab3/cookie">Куки</a></li>
                </ul>

                <footer>
                    <p>Киценко Анастасия Валерьевна</p>
                    <p>ФБИ-21, Факультет ФБ, 2024 год</p>
                </footer>
            </body>
        </html>
    '''