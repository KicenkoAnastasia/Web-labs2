from flask import Flask
app = Flask (__name__)

@app.route("/")
def start(): 
    return """<!doctype html>
        <html>
           <body>
               <h1>Wev-серверна flask</h1>
           </body>
        </html>"""
