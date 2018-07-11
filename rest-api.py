from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import requests, winsound as ws, threading, service as srv, match, time
from vlc import MediaPlayer

app = Flask(__name__)
m = match.Match()
previous_chal = {'id': -1}
music_player = MediaPlayer("static/music trivia/payday.mp3")
music_on = False
@app.route('/')
def lobby():
    return redirect(url_for('showPlayers'))


@app.route('/categories')
def categories():
    r = requests.get(m.ONLINE_SERVER + "/categories")
    r = r.json()
    return render_template('categories.html', res=r)


@app.route('/viewChallenge/<challenge>')
def viewChallenge(challenge):
    global previous_chal
    result = requests.get(m.ONLINE_SERVER + "/getChallenge/" + challenge)
    json = result.json()
    trivia = int(json['trivia'])
    if trivia == 1:
        info = requests.post(m.ONLINE_SERVER + "/getQuiz/" + challenge, json={'list': m.quiz}).json()
        info_list = [info['answer'], info['wrong1'], info['wrong2'], info['wrong3']]
        size = len(info_list)
        info_list = srv.randomize(info_list)

        answer = ""
        for i in range(0, size):
            if info['answer'] == info_list[i]:
                answer = i

        m.updateTrivia({'chal_id': info['chal_id'], 'q_id': info['q_id'], 'answer': answer})
        resource = info['resource']
        info = [info['chal_id'], info['q_id'], info['question']] + info_list + [resource.replace(' ', '_')]
    else:
        m.updateTrivia(None)
        info = ""
        size = -1

    if previous_chal['id'] != m.current_chal['id']:
        previous_chal = dict(m.current_chal)
        m.sendNotifications()
    return render_template('challenges.html', res=json, info=info, size_info=size, players=m.player_turn, active=m.current_chal['active'],
                           p_number= len(m.player_turn))


@app.route('/players')
def showPlayers():
    return render_template('lobby.html', players=m.getPlayersName(), admin=m.admin, n=len(m.players))


@app.route('/endgame')
def endgame():
    return render_template('endgame.html')


@app.route('/playMusic')
def playMusic():
    global music_on
    if not music_on:
        music_player.play()
        music_on = True
    return jsonify({"result": "SUCCESS"})

@app.route('/stopMusic')
def stopMusic():
    global music_on
    if music_on:
        music_player.pause()
        music_on = False
    return jsonify({"result": "SUCCESS"})

# MOBILE
@app.route('/categoriesM')
def categoriesM():
    result = requests.get(m.ONLINE_SERVER + "/categories")
    threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/categories")).start()
    m.setActiveMatch(True)
    tmp = result.json()
    tmp['result'] = 1
    return jsonify(tmp)


# MOBILE
@app.route('/getChallenge/<category>')
def getChallenge(category):
    r = requests.post(m.ONLINE_SERVER + "/getChallenge/" + category, json={'list': m.played_chal})
    if r.text == "-1":
        threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/endgame")).start()
        m.sendNotifications()
        return jsonify({'result': -1})

    json = r.json()
    if json['id'] == 1:
        m.playerTurn(len(m.players))
    else:
        m.playerTurn(1)
    m.updateChallenge(json)
    m.setActive(m.current_chal, False)
    m.setCategory(json['type'])
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

    # Check if the user already joined
    if m.containsPlayer(json['username']):
        if m.admin == json['username']:
            m.sendNotifications([json['username']])
            return jsonify({"result": "SUCCESS", "admin": True, "active": m.active})
        else:
            m.sendNotifications([json['username']])
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
        return jsonify({"result": "SUCCESS", "admin": False, "active": m.active})
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
                # If the player answer correctly HOMMY provides a new Quiz
                ws.PlaySound(correct, ws.SND_FILENAME | ws.SND_ASYNC)
                threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(chal_id))).start()
                return jsonify({'result': "CORRECT"})
            else:
                # If the player answer wrongly HOMMY provides a new Quiz and change player turn
                ws.PlaySound(wrong, ws.SND_FILENAME | ws.SND_ASYNC)
                time.sleep(2)
                if m.playerTurn(1) == -1:
                    # Manda notifica per far fare il refresh challenge
                    getChallenge(m.getCategory())
                else:
                    m.setActive(m.current_chal, False)
                    threading.Thread(target=srv.openWebPage,args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(chal_id))).start()
                return jsonify({'result': "WRONG"})

    return jsonify({'result': "NOT AUTHORIZED"})


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

# MOBILE
@app.route('/startchallenge/<int:id>')
def startChallenge(id):
    global music_on
    user = request.headers['authorization']
    found = False
    for p in m.player_turn:
        if user == p:
            found = True
            # Check if the challenge has already began
            if not m.isActive(m.current_chal):
                m.setActive(m.current_chal, True)
                threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(id))).start()
                music_on = False
                music_player.pause()
                return jsonify({'result': 1})

    if found is False:
        return jsonify({'result': -1})

    music_on = False
    music_player.pause()
    return jsonify({'result': 2})

# MOBILE
@app.route('/do/<int:challenge>')
def do(challenge):
    user = request.headers['authorization']
    found = False
    for p in m.player_turn:
        if user == p:
            found = True
    if found is False:
        return jsonify({"result": "NOT AUTHORIZED"})

    if int(challenge) == 2:
        freq = m.getVoiceHzResult(user)
        if freq == -1:
            freq = srv.randomFrequency()
            m.voiceHzResult(user,freq)
        threading.Thread(target=ws.Beep, args=(freq,5000)).start()

    return jsonify({"result": "SUCCESS"})


# MOBILE
@app.route('/challengeResult', methods=['POST'])
def challengeResult():
    global music_on
    res = request.json
    user = request.headers['authorization']
    found = False
    for p in m.player_turn:
        if user == p:
            found = True
    if found is False:
        return jsonify({"result": "NOT AUTHORIZED"})
    id = res['id']

    if id == 1:
        for key in res:
            if key != 'id':
                # Calcolo punteggio per tempi
                print(key+": " + str(res[key]))
        time.sleep(2)
        m.setActive(m.current_chal, False)
        getChallenge(m.getCategory())
    elif id == 2:
        given_freq = m.getVoiceHzResult(user)
        recorded_freq = res['frequency']
        # Calculate the error between the two frequency assign a score to the performance, and set a winner

        if m.playerTurn(1) == -1:
            # Manda notifica per far fare il refresh challenge
            getChallenge(m.getCategory())
        else:
            m.setActive(m.current_chal, False)
            threading.Thread(target=srv.openWebPage,args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(id))).start()

        music_on = True
        music_player.play()

    elif id == 3:
        pass
    elif id == 4:
        pass
    else:
        return jsonify({"result": "INVALID CHALLENGE"})

    return jsonify({"result": "SUCCESS"})


if __name__ == '__main__':
    app.run()
