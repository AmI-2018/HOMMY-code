from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import requests, winsound as ws, threading, service as srv, match, time
from vlc import MediaPlayer

app = Flask(__name__)
m = match.Match()
previous_chal = {'id': -1}
music_player = MediaPlayer("static/music trivia/payday.mp3")
music_on = False
ready = 0
feedback = {"times": 0, "rate": 0}

RIGHT_ANSWER = 100
VOICE_HZ = {5: 1000, 50: 500, 100: 400, 150: 300, 250: 100, 350: 20}
FITNESS_CHAL_MULTIPLIER = 5

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
    global ready
    r = requests.post(m.ONLINE_SERVER + "/getChallenge/" + category, json={'list': m.played_chal})
    if r.text == "-1":
        threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/endgame")).start()
        m.sendNotifications()
        return jsonify({'result': -1})

    json = r.json()
    lastChal = m.getCurrentIdChal()
    if json['id'] == 1:
        m.playerTurn(len(m.players))
    elif (lastChal != 2) and (lastChal !=4):
        m.playerTurn(1)

    m.updateChallenge(json)
    m.setActive(m.current_chal, False)
    ready = 0
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
    global ready
    correct = 'static\sound effects\Correct Answer.wav'
    wrong = 'static\sound effects\Wrong Answer.wav'
    if chal_id != m.current_trivia['chal_id']:
        abort(409)

    user = request.headers['authorization']
    current_player = m.getPlayer(user)
    # Calcolo indice risposta attraverso i codici ascii
    a = ord(answer.lower()) - ord("a")
    for p in m.player_turn:
        if user == p:
            if m.current_trivia['answer'] == a:
                # If the player answer correctly HOMMY provides a new Quiz
                ws.PlaySound(correct, ws.SND_FILENAME | ws.SND_ASYNC)
                current_player.addPoints(RIGHT_ANSWER, 4)
                threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(chal_id))).start()
                return jsonify({'result': "CORRECT"})
            else:
                # If the player answer wrongly HOMMY provides a new Quiz and change player turn
                current_player.resetCorrectAnswer()
                print(user + ": " + str(current_player.getScore()))
                ws.PlaySound(wrong, ws.SND_FILENAME | ws.SND_ASYNC)
                time.sleep(2)
                if m.playerTurn(1) == -1:
                    # Manda notifica per far fare il refresh challenge
                    getChallenge(m.getCategory())
                else:
                    ready = 0
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
    global ready
    user = request.headers['authorization']
    found = False
    for p in m.player_turn:
        if user == p:
            found = True
            ready = ready + 1
            # Check if the challenge has already began
            if (not m.isActive(m.current_chal)) and (ready == len(m.player_turn)):
                m.setActive(m.current_chal, True)
                threading.Thread(target=srv.openWebPage, args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(id))).start()
                stopMusic()

                return jsonify({'result': 1})

    if found is False:
        return jsonify({'result': -1})

    stopMusic()
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
    global ready
    res = request.json
    user = request.headers['authorization']

    found = False
    for p in m.player_turn:
        if user == p:
            found = True
    if found is False:
        return jsonify({"result": "NOT AUTHORIZED"})
    id = res['id']
    # FITNESS CHALLENGE
    if id == 1:
        for key in res:
            if key != 'id':
                # Calcolo punteggio per tempi
                current_player = m.getPlayer(key)
                print(key+": " + str(res[key]))
                if res[key] == 0:
                    current_player.addPoints(600)
                else:
                    current_player.addPoints(int(res[key] * FITNESS_CHAL_MULTIPLIER))
                print(current_player.getScore())

        time.sleep(2)
        m.setActive(m.current_chal, False)
        getChallenge(m.getCategory())
    # VOICE HZ DETECTOR
    elif id == 2:
        current_player = m.getPlayer(user)
        given_freq = m.getVoiceHzResult(user)
        recorded_freq = res['frequency']
        diff = abs(recorded_freq-given_freq)

        # Calculate the error between the two frequency and assign a score to the performance, and set a winner
        points = list(VOICE_HZ)
        points.sort()

        for i in points:
            if diff < i:
                current_player.addPoints(VOICE_HZ[i])
                break
        print(user + ": " + str(current_player.getScore()))

        if m.playerTurn(1) == -1:
            # Manda notifica per far fare il refresh challenge
            getChallenge(m.getCategory())
        else:
            m.setActive(m.current_chal, False)
            ready = 0
            threading.Thread(target=srv.openWebPage,args=(m.driver, m.THIS_SERVER + "/viewChallenge/" + str(id))).start()

        playMusic()
    # DANCE AND STOP
    elif id == 3:
        pass
    # MUSIC TRIVIA
    elif id == 4:
        pass
    else:
        return jsonify({"result": "INVALID CHALLENGE"})

    return jsonify({"result": "SUCCESS"})

@app.route('/feedback/<int:chal_id>', methods=['POST'])
def feedback(chal_id):
    global feedback
    user = request.headers['authorization']

    found = False
    for p in m.player_turn:
        if user == p:
            found = True
    if found is False:
        return jsonify({"result": "NOT AUTHORIZED"})

    json = request.json
    feedback['times'] = feedback['times'] + 1
    feedback['rate'] = feedback['rate'] + int(json['rate'])

    if feedback['times'] == len(m.players):
        res = requests.post(m.ONLINE_SERVER + "/feedback/" + str(chal_id), json=feedback)
        feedback['times'] = 0
        feedback['rate'] = 0
        getChallenge(m.getCategory())
        return jsonify({'result': res.text})

    return jsonify({"result": "SUCCESS"})



if __name__ == '__main__':
    app.run()
