from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests, webbrowser
app = Flask(__name__)
ONLINE_SERVER = "http://127.0.0.1:5000"
THIS_SERVER = "http://192.168.1.111:5000"

@app.route('/')
def hello_world():
    return redirect(url_for('index'))


@app.route('/categories')
def categories():
    r = requests.get(ONLINE_SERVER + "/categories")
    return render_template('categories.html', res = r.json())

@app.route('/categoriesM')
def categoriesM():
    webbrowser.open(THIS_SERVER + "/categories")
    return "Ciao"

if __name__ == '__main__':
    app.run()