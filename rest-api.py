from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import requests, winsound as ws, threading, service as srv

app = Flask(__name__)
app.secret_key = "alksjd@1'fjksjdh3mnjnrmajkr092i'#"
ONLINE_SERVER = "http://127.0.0.1:5000"
THIS_SERVER = "http://192.168.1.111:5000"
MAX_PLAYERS = 8
players = list()
played_chal = list()
admin = ''
current_trivia = ''

@app.route('/')
def lobby():
    return redirect(url_for('showPlayers'))


@app.route('/categories')
def categories():
    r = requests.get(ONLINE_SERVER + "/categories")
    return render_template('categories.html', res=r.json())


@app.route('/viewChallenge/<challenge>')
def viewChallenge(challenge):
    result = requests.get(ONLINE_SERVER + "/getChallenge/" + challenge)
    json = result.json()
    trivia = int(json['challenges'][0]['trivia'])

    if trivia == 1:
        current_trivia = requests.get(ONLINE_SERVER + "/getQuiz/" + challenge).json()
        info = dict(current_trivia)
        info_list = [info['answer'], info['wrong1'], info['wrong2'], info['wrong3']]
        info_list = srv.randomize(info_list)
        info = [info['q_id'], info['question']] + info_list
        size = len(info_list)
    else:
        info = ""
        size = -1
    return render_template('challenges.html', res=json, info=info, size_info=size)


@app.route('/players')
def showPlayers():
    return render_template('lobby.html', players=players, admin=admin, n=len(players))


@app.route('/endgame')
def endgame():
    return render_template('endgame.html')


@app.route('/do/<int:challenge>')
def do(challenge):
    if int(challenge)==2:
        ws.Beep(1000, 1000)
    return "success"


@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    psw = request.form['psw']
    json = {'username': user, 'psw': psw}
    result = requests.post(ONLINE_SERVER + "/login", json=json)

    if result.text != "WRONG" and result.text != "ERROR JSON":
        session['username'] = user
        return redirect(url_for('lobby'))

    return "USERNAME O PASSWORD ERRATI"


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('hello_world'))


@app.route('/signin', methods=['GET', 'POST'])
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


# MOBILE
@app.route('/categoriesM')
def categoriesM():
    result = requests.get(ONLINE_SERVER + "/categories")
    threading.Thread(target=srv.categories).start()
    return jsonify(result.json())


# MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.post(ONLINE_SERVER + "/getChallenge/" + category, json={'list': played_chal})
    if r.text == "-1":
        threading.Thread(target=srv.endGame).start()
        return "SFIDE TERMINATE"
    json = r.json()
    chal_id = str(json['challenges'][0]['id'])
    played_chal.append(int(chal_id))
    threading.Thread(target=srv.challenge, args=(chal_id,)).start()
    return jsonify(r.json())


# MOBILE
@app.route('/join', methods=['POST'])
def joinMatch():
    global admin
    json = request.json
    if(json is None) or ('username' not in json):
        return "ERROR USER"
    if len(players) == 0:
        players.append(json['username'])
        admin = json['username']
        threading.Thread(target=srv.players).start()
        return "ADMIN"
    elif len(players) < MAX_PLAYERS:
        players.append(json['username'])
        threading.Thread(target=srv.players).start()
    else:
        return "LIMITE GIOCATORI RAGGIUNTO"
    return "SUCCESS"


if __name__ == '__main__':
    app.run()
