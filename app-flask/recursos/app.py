from flask import Flask
from recursos.routes.routes import *

app = Flask(__name__)

#rutas de la aplicacion
app.add_url_rule(routes["hello_route"], view_func=routes["hello_controller"])

#Ruta del error 404
app.register_error_handler(routes["not_found_route"], routes["not_found_controller"])

@app.route('/404')
def index():
    return render_template('404.html')
