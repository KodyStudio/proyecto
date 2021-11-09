from flask import Flask, render_template, request
from recursos.db import mysql
from flask.views import MethodView

class HelloController(MethodView):
    def get(self):
        return render_template('index.html')

def post(self):
    code = request.form['code']
    name = request.form['name']
    stock = request.form['stock']
    value = request.form['value']
    category = request.form['category']   
    
    print(code, name, stock, value, category)     
    return "method post is work"