from flask import Flask, render_template, redirect, url_for, request
import requests
app = Flask(__name__)
ONLINE_SERVER = "127.0.0.1:5000";

@app.route('/')
def hello_world():
    return redirect(url_for('index'))


@app.route('/categories')
def index():
    result = requests.get(ONLINE_SERVER + "/categories")
    return render_template('categories.html', res = result)

if __name__ == '__main__':
    app.run()