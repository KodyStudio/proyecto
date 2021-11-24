import os

import requests
from dotenv import load_dotenv
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy.sql.elements import Null
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from flask import jsonify

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

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


@app.route('/registro', methods=["GET", "POST"])
def register():

    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']

    # creacion del cursor
    # cur = mysql.connection.cursor()

    # mysql.connection.commit()

    # contrasena_enconde = contrasena.encode("utf-8")
    # contrasena_encriptado = bcrypt.hashpw(contrasena_encode, semilla)

    return render_template('registro.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
