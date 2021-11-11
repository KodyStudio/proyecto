from flask import Flask, render_template
app = Flask(__name__)  
 
@app.route('/')  
def home():  
    return render_template('index.html'); 

@app.route('/home/add_product')  
def add_product():  
    return render_template('page-add-product.html');   

@app.route('/home/error')  
def error():  
    return render_template('404.html');  
  
if __name__ =="__main__":  
    app.run(debug = True)  


