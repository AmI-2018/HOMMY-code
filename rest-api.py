from flask import Flask, render_template, redirect, url_for, request, jsonify, session, abort
import requests, winsound as ws, threading, service as srv, match

app = Flask(__name__)
app.secret_key = "alksjd@1'fjksjdh3mnjnrmajkr092i'#"

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
    trivia = int(json['challenges'][0]['trivia'])
    print(trivia)
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
        info = ""
        size = -1
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



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('lobby'))



# MOBILE
@app.route('/categoriesM')
def categoriesM():
    result = requests.get(m.ONLINE_SERVER + "/categories")
    threading.Thread(target=srv.categories, args=(m.driver, m.THIS_SERVER + "/categories")).start()
    return jsonify(result.json())


# MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.post(m.ONLINE_SERVER + "/getChallenge/" + category, json={'list': m.played_chal})
    if r.text == "-1":
        threading.Thread(target=srv.endGame, args=(m.driver, m.THIS_SERVER + "/endgame")).start()
        return "SFIDE TERMINATE"
    m.playerTurn(2)
    json = r.json()
    chal_id = str(json['challenges'][0]['id'])
    m.played_chal.append(int(chal_id))
    threading.Thread(target=srv.challenge, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + chal_id)).start()
    return jsonify(r.json())


# MOBILE
@app.route('/join', methods=['POST'])
def joinMatch():
    json = request.json
    if(json is None) or ('username' not in json):
        return "ERROR USER"
    if len(m.players) == 0:
        m.newPlayer(json['username'])
        m.setAdmin(json['username'])
        threading.Thread(target=srv.players, args=(m.driver, m.THIS_SERVER + "/players")).start()
        return "ADMIN"
    elif len(m.players) < m.MAX_PLAYERS:
        m.newPlayer(json['username'])
        threading.Thread(target=srv.players, args=(m.driver, m.THIS_SERVER + "/players")).start()
    else:
        return "LIMITE GIOCATORI RAGGIUNTO"
    return "SUCCESS"

# MOBILE
@app.route('/answer/<int:chal_id>/<answer>')
def chooseAnswer(chal_id, answer):
    if chal_id != m.current_trivia['chal_id']:
        abort(409)

    user = request.headers['authorization']
    #Calcolo indice risposta attraverso i codici ascii
    a = ord(answer.lower()) - ord("a")
    for p in m.player_turn:
        if user == p:
            if m.current_trivia['answer'] == a:
                return user + " RISPOSTA CORRETTA"
            else:
                return user + " RISPOSTA ERRATA"

    abort(401)


#MOBILE
@app.route('/login', methods=['POST'])
def login():
    info = request.json
    result = requests.post(m.ONLINE_SERVER + "/login", json=info)

    if result.text != "WRONG" and result.text != "ERROR JSON":
        tmp = result.json()
        tmp['result'] = 1
        return jsonify(tmp)

    return jsonify({"result": -1})


@app.route('/signin', methods=['POST'])
def signin():
    info = request.json
    res = requests.post(m.ONLINE_SERVER + "/signin", json=info)
    return jsonify({"result": res.text})

@app.route('/provaPost', methods=['POST'])
def provaPost():
    info = request.headers
    print(info)

    return "SUCCESS"

if __name__ == '__main__':
    app.run()
