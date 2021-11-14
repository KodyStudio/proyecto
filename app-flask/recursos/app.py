from flask import Flask, render_template
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///register.db")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home/add_product')
def add_product():
    return render_template('page-add-product.html')


@app.route('/home/error')
def error():
    return render_template('404.html')


@app.route('/home/base')
def base():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
