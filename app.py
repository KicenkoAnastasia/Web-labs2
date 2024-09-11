from flask import Flask
app = Flask (__name__)


@app.route("/web")
def web(): 
    return """<!doctype html>
        <html>
           <body>
               <h1>Wev-серверна flask</h1>
           </body>
        </html>"""

@app.route("/author")
def author():
    name = 'Киценко Анастасия Валерьевна'
    group = 'ФБИ-21'
    faculty = 'ФБ'

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
            </body>
        </html>"""