from flask import Flask, render_template, url_for, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/guestbook')
def guestbook():
    return render_template("guestbook.html")