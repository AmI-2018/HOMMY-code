from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests, webbrowser
import time
app = Flask(__name__)
ONLINE_SERVER = "http://127.0.0.1:5000"
THIS_SERVER = "http://192.168.1.111:5000"

@app.route('/')
def hello_world():
    return redirect(url_for('categories'))


@app.route('/categories')
def categories():
    r = requests.get(ONLINE_SERVER + "/categories")
    return render_template('categories.html', res = r.json())

#MOBILE
@app.route('/categoriesM')
def categoriesM():

    result = requests.get(ONLINE_SERVER + "/categories")
    webbrowser.open(THIS_SERVER + "/categories")
    return jsonify(result.json())

@app.route('/viewChallenge/<challenge>')
def viewChallenge(challenge):
    return render_template('challenges.html', res= challenge)

#MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.get(ONLINE_SERVER + "/getChallenge/" + category)
    json = r.json()
    webbrowser.open(THIS_SERVER + '/viewChallenge/' + str(json['challenges'][0]['id']))
    return jsonify(r.json())

if __name__ == '__main__':
    app.run()