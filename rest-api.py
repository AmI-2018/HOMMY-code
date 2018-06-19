from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import requests, winsound as ws, threading, service as srv, match

app = Flask(__name__)
m = match.Match()

@app.route('/')
def lobby():
    return redirect(url_for('showPlayers'))


@app.route('/categories')
def categories():
    r = requests.get(m.ONLINE_SERVER + "/categories")
    return render_template('categories.html', res=r.json())


@app.route('/viewChallenge/<challenge>')
def viewChallenge(challenge):
    result = requests.get(m.ONLINE_SERVER + "/getChallenge/" + challenge)
    json = result.json()
    trivia = int(json['trivia'])
    if trivia == 1:
        info = requests.get(m.ONLINE_SERVER + "/getQuiz/" + challenge).json()
        info_list = [info['answer'], info['wrong1'], info['wrong2'], info['wrong3']]
        size = len(info_list)
        info_list = srv.randomize(info_list)

        answer = ""
        for i in range(0, size):
            if info['answer'] == info_list[i]:
                answer = i

        m.updateTrivia({'chal_id': info['chal_id'], 'q_id': info['q_id'], 'answer': answer})
        info = [info['chal_id'], info['q_id'], info['question']] + info_list
    else:
        m.updateTrivia(None)
        info = ""
        size = -1

    m.sendNotifications(m.getToken(m.admin))
    return render_template('challenges.html', res=json, info=info, size_info=size, players=m.player_turn)


@app.route('/players')
def showPlayers():
    return render_template('lobby.html', players=m.players, admin=m.admin, n=len(m.players))


@app.route('/endgame')
def endgame():
    return render_template('endgame.html')


@app.route('/do/<int:challenge>')
def do(challenge):
    if int(challenge)==2:
        ws.Beep(1000, 1000)
    return "success"


# MOBILE
@app.route('/categoriesM')
def categoriesM():
    result = requests.get(m.ONLINE_SERVER + "/categories")
    threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/categories")).start()
    m.setActive(True)
    tmp = result.json()
    tmp['result'] = 1
    return jsonify(tmp)


# MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.post(m.ONLINE_SERVER + "/getChallenge/" + category, json={'list': m.played_chal})
    if r.text == "-1":
        threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/endgame")).start()
        return jsonify({'result': -1})
    m.playerTurn(1)
    json = r.json()
    m.updateChallenge(json)
    chal_id = str(json['id'])
    m.played_chal.append(int(chal_id))
    threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + chal_id)).start()
    json['result'] = 1
    return jsonify(json)


# MOBILE
@app.route('/currentChallenge')
def currentChallenge():
    headers = request.headers
    tmp = dict(m.current_chal)
    if m.active and m.containsPlayer(headers['authorization']):
        tmp['result'] = 1
        return jsonify(tmp)

    tmp['result'] = -1
    return jsonify(tmp)


# MOBILE
@app.route('/join', methods=['POST'])
def joinMatch():
    json = request.json
    if(json is None) or ('username' not in json):
        return jsonify({"result": "ERROR USER"})
    print(json['token'])
    # Check if the user already joined
    if m.containsPlayer(json['username']):
        if m.admin == json['username']:
            return jsonify({"result": "SUCCESS", "admin": True, "active": m.active})
        else:
            return jsonify({"result": "SUCCESS", "admin": False, "active": m.active})

    # Check if he's the first one
    if len(m.players) == 0:
        m.newPlayer(json['username'], json['token'])
        m.setAdmin(json['username'])
        threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/players")).start()
        return jsonify({"result": "SUCCESS", "admin": True, "active": m.active})

    # Check if players filled the match
    elif len(m.players) < m.MAX_PLAYERS:
        m.newPlayer(json['username'], json['token'])
        threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/players")).start()
        return jsonify({"result": "SUCCESS", "admin": False})
    else:
        return jsonify({"result": "LIMITE GIOCATORI RAGGIUNTO", "active": m.active})


# MOBILE
@app.route('/answer/<int:chal_id>/<answer>')
def chooseAnswer(chal_id, answer):
    correct = 'static\sound effects\Correct Answer.wav'
    wrong = 'static\sound effects\Wrong Answer.wav'
    if chal_id != m.current_trivia['chal_id']:
        abort(409)

    user = request.headers['authorization']
    # Calcolo indice risposta attraverso i codici ascii
    a = ord(answer.lower()) - ord("a")
    for p in m.player_turn:
        if user == p:
            if m.current_trivia['answer'] == a:
                ws.PlaySound(correct, ws.SND_FILENAME | ws.SND_ASYNC)
                return jsonify({'result': "CORRECT"})
            else:
                ws.PlaySound(wrong, ws.SND_FILENAME | ws.SND_ASYNC)
                return jsonify({'result': "WRONG"})

    abort(401)


# MOBILE
@app.route('/login', methods=['POST'])
def login():
    info = request.json
    result = requests.post(m.ONLINE_SERVER + "/login", json=info)

    if result.text != "WRONG" and result.text != "ERROR JSON":
        tmp = result.json()
        tmp['result'] = 1
        return jsonify(tmp)

    return jsonify({"result": -1})


# MOBILE
@app.route('/signin', methods=['POST'])
def signin():
    info = request.json
    res = requests.post(m.ONLINE_SERVER + "/signin", json=info)
    return jsonify({"result": res.text})


if __name__ == '__main__':
    app.run()
