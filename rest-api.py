from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import requests, webbrowser, winsound as ws

app = Flask(__name__)
app.secret_key = "alksjd@1'fjksjdh3mnjnrmajkr092i'#"
ONLINE_SERVER = "http://127.0.0.1:5000"
THIS_SERVER = "http://192.168.1.111:5000"
players=[]
admin=''

@app.route('/')
def hello_world():
    username = session.get('username', '')
    return render_template('index.html', name= username)


@app.route('/categories')
def categories():
    r = requests.get(ONLINE_SERVER + "/categories")
    return render_template('categories.html', res = r.json())

@app.route('/viewChallenge/<challenge>')
def viewChallenge(challenge):
    result = requests.get(ONLINE_SERVER + "/getChallenge/" + challenge)
    json = result.json()

    return render_template('challenges.html', res = json)

@app.route('/players')
def showPlayers():
    return render_template('players.html', players= players)

@app.route('/do/<int:challenge>')
def do(challenge):
    if(int(challenge) == 2):
        ws.Beep(1000, 1000)
    return "success"

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    psw = request.form['psw']
    json = {'username': user, 'psw': psw}
    result = requests.post(ONLINE_SERVER + "/login", json = json)

    if result.text != "WRONG" and result.text != "ERROR JSON":
        session['username'] = user
        return redirect(url_for('hello_world'))

    return "USERNAME O PASSWORD ERRATI"

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('hello_world'))

@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method == "GET":
        if session.get('username'):
            return redirect(url_for('hello_world'))
        else:
            return render_template('signin.html')

    elif request.method == "POST":
        user = request.form['username']
        psw = request.form['psw']
        date = request.form['date']
        genre = request.form['genre']
        json = {"username": user, "psw": psw, "birth": date, "genre": genre}
        res = requests.post(ONLINE_SERVER + "/signin", json=json)
        return res.text

#MOBILE
@app.route('/categoriesM')
def categoriesM():

    result = requests.get(ONLINE_SERVER + "/categories")
    webbrowser.open(THIS_SERVER + "/categories")
    return jsonify(result.json())

#MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.get(ONLINE_SERVER + "/getChallenge/" + category)
    json = r.json()
    webbrowser.open(THIS_SERVER + '/viewChallenge/' + str(json['challenges'][0]['id']))
    return jsonify(r.json())

#MOBILE
@app.route('/join', methods=['POST'])
def joinMatch():
    json = request.json
    if(json is None) or ('username' not in json):
        return "ERROR USER"
    if len(players)==0:
        players.append(json['username'])
        admin = json['username']
        return "ADMIN"
    elif(len(players) < 8):
        players.append(json['username'])
        webbrowser.open(THIS_SERVER+"/players")
    else:
        return "LIMITE GIOCATORI RAGGIUNTO"
    return "SUCCESS"


if __name__ == '__main__':
    app.run()