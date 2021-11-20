from re import M
from flask import Flask, render_template, request
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
# import pymysql

app = Flask(__name__)

# La llave secreta
app.secret_key = "applogin"

# semilla para encriptamiento
semilla = bcrypt.gensalt()

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'register'
# mysql = MySQL(app)


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
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        # creacion del cursor
        # cur = mysql.connection.cursor()

        # mysql.connection.commit()

        # contrasena_enconde = contrasena.encode("utf-8")
        # contrasena_encriptado = bcrypt.hashpw(contrasena_encode, semilla)

    return render_template('resgistro.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
