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


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return flash("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return flash("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return flash("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if request.method == "POST":
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     confirmation = request.form.get('confirmation')
    #     # sustituir los apology por flash cuando hay un error y rederizar a registro.html
    #     if not username:
    #         return flash("Username es requerido")
    #     elif not password:
    #         return flash("Password es requerido")
    #     elif not confirmation:
    #         return flash("Confirmation es requerido")

    #     if password != confirmation:
    #         return flash("Password no coinciden bro xd")

    #     userid = db.execute("SELECT * FROM users WHERE username = ?", username)

    #     if len(userid) == 1:
    #         return flash("hay un usuario con ese name UnU")
    #     else:
    #         hash = generate_password_hash(password)

    #         id_user = db.execute(
    #             "INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)
    #         session["user_id"] = id_user
    #         flash("registrado")
    #         return redirect('/')

    # else:
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
