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


@app.route('/', methods=["GET", "POST"])
@login_required
def home():

    user = db.execute(f"SELECT * FROM users WHERE id = :id",
                      {"id": session["user_id"]}).fetchone()["username"]

    return render_template('index.html', user=user)


@app.route("/home/add_product", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        costo = request.form.get("costo")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        id_categoria = request.form.get("categoria")
        url = request.form.get("url")
        descripcion = request.form.get("descripcion")

        db.execute("INSERT INTO productos (nombre, costo, precio, id_categoria, imagen, descripcion, cantidad) VALUES (:nombre, :costo, :precio, :id_categoria, :imagen, :descripcion, :cantidad)", {
                   "nombre": nombre, "costo": costo, "precio": precio, "id_categoria": id_categoria, "imagen": url, "descripcion": descripcion, "cantidad": cantidad})
        db.commit()

        flash("producto agregado")
        return redirect("/")

    else:

        user = db.execute("SELECT * FROM users WHERE id = :id",
                          {"id": session["user_id"]}).fetchone()["username"]

        categorias = db.execute(
            "SELECT * FROM categorias WHERE nombre ilike '%%'")
        return render_template("add-product.html", user=user, categorias=categorias)


@app.route('/home/list_product')
@login_required
def list_product():

    lista = db.execute(
        "SELECT p.id AS id, p.id_categoria, p.nombre, costo, precio, cantidad, descripcion, imagen, c.id AS idcategoria, c.nombre AS categoria FROM productos p inner join categorias c on p.id_categoria=c.id")

    user = db.execute("SELECT * FROM users WHERE id = :id",
                      {"id": session["user_id"]}).fetchone()["username"]

    return render_template('list-product.html', lista=lista, user=user)


@app.route('/eliminar_productos/<id>')
@login_required
def eliminar_productos(id):

    db.execute("DELETE FROM productos WHERE id=:id", {"id": id})
    db.commit()

    flash("xd")
    return redirect('/')


@app.route('/mensaje', methods=["GET"])
@login_required
def mensaje():

    return render_template("message.html")

@app.route('/getjson', methods=["GET"])
def getjson():

    ap = db.execute("SELECT * FROM productos").fetchall()

    otra = []
    for nombre in ap:


        data = {
            "id":nombre['id'],
            "nombre": nombre["nombre"],
            "imagen": nombre["imagen"],
            "precio": nombre["precio"],


                }


        otra.append(data)

    return jsonify(otra)
@app.route("/modal", methods=["GET"])
def modal():
    return render_template("modal.html")


@app.route('/home/add_sale')
@login_required
def add_sale():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        imagen = request.form.get("imagen")
        descripcion = request.form.get("descripcion")

    else:

        user = db.execute("SELECT * FROM users WHERE id = :id",
                          {"id": session["user_id"]}).fetchone()["username"]

        platillos = db.execute(
            "SELECT * FROM platillos")

        return render_template('add-sale.html', user=user)


@app.route('/home/add_platillo')
@login_required
def add_platillo():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        imagen = request.form.get("imagen")
        descripcion = request.form.get("descripcion")

    else:
        return render_template('add-platillo.html')


@app.route('/home/error')
@login_required
def error():
    return render_template('404.html')


@app.route('/home/base')
@login_required
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
            flash("Username es requerido")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password es requerido")
            return render_template("login.html")

        # Query database for username

        count = 0
        hash = Null
        id = 0

        for rows in db.execute("SELECT count(username), hash, id FROM users WHERE username = :username GROUP BY username, id, hash",
                               {"username": request.form.get("username")}):
            count = rows[0]
            hash = rows['hash']
            id = rows['id']

        print(count)

        # Ensure username exists and password is correct
        if count == 0 or not check_password_hash(hash, request.form.get("password")):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = id

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
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        # sustituir los apology por flash cuando hay un error y rederizar a registro.html
        if not username:
            flash("Username es requerido")
            return render_template("register.html")
        elif not password:
            flash("Password es requerido")
            return render_template("register.html")
        elif not confirmation:
            flash("Confirmation es requerido")
            return render_template("register.html")

        if password != confirmation:
            flash("Password no coinciden bro")
            return render_template("register.html")

        userid = db.execute(
            f"SELECT * FROM users WHERE username = '{request.form.get('username')}'").rowcount

        if userid > 0:
            flash("hay un usuario con ese name UnU")
            return render_template("register.html")

        hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)", {"username": username, "hash": hash})
        db.commit()
        id_user = db.execute("SELECT id FROM users WHERE username=:username",
                             {"username": username, "hash": hash}).fetchone()["id"]
        session["user_id"] = id_user
        flash("registrado")
        return redirect('/')

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
