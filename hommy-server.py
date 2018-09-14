from flask import Flask, render_template, url_for, redirect, jsonify, request
import db
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/categories', methods=['GET'])
def categories():
    res = db.showCategories()
    categories = []

    for c in res:
        cat = prepare_cat_json(c)
        categories.append(cat)

    return jsonify({'categories': categories})

@app.route('/getChallenge/<category>', methods=['POST'])
def getRandomChallenge(category):
    chal_list = request.json
    res = db.getRandomChallenge(category, chal_list['list'])
    if res == -1:
        return str(res)

    res = prepare_chal_json(res)
    return jsonify(res)

@app.route('/getChallenge/<int:id>', methods=['GET'])
def getChallenge(id):
    res = db.getChallenge(id)

    res = prepare_chal_json(res)
    return jsonify(res)

@app.route('/getQuiz/<int:id>', methods=['POST'])
def getRandomQuiz(id):
    quiz_list = request.json
    res = db.getRandomQuiz(id, quiz_list['list'])

    quiz = {
        'chal_id': res[0],
        'q_id': res[1],
        'question': res[2],
        'answer': res[3],
        'wrong1': res[4],
        'wrong2': res[5],
        'wrong3': res[6],
        'resource': res[7]
    }
    return jsonify(quiz)

@app.route('/login', methods=['POST'])
def login():
    json = request.json

    if (json is not None) and ('username' in json) and ('psw' in json):
        res = db.getUserInfo(json['username'], json['psw'])
        if res is not None:
            return jsonify(prepare_user_json(res))
        return "WRONG"

    return "ERROR JSON"

@app.route('/signin', methods=['POST'])
def signin():
    json = request.json
    if (json is not None) and ('username' in json) and ('psw' in json) and ('birth' in json):
        return db.registerUser(json['username'], json['psw'], json['birth'], json['genre'])

    return "ERROR JSON"

@app.route('/feedback/<int:chal_id>', methods=['POST'])
def feedback(chal_id):
    json = request.json
    if (json is not None) and ('rate' in json) and (int(json['rate']) != 0):
        return db.rate(chal_id, int(json['rate']))

    return "ERROR JSON"


@app.route('/getRanking/<int:chal_id>')
def ranking(chal_id):
   res = db.getRanking(chal_id)
   lista = list()
   for score in res:
       lista.append(score[0]+ ' -> ' + str(score[1]))

   return jsonify({'result':"SUCCESS", 'scores': lista})


@app.route('/updateBestScore', methods=['POST'])
def updateBestScore():
    json = request.json
    if (json is not None) and ('username' in json) and ('chal_id' in json) and ('score' in json):
        return db.bestScore(json['username'], json['chal_id'], json['score'])

    return "ERROR JSON"

def prepare_cat_json(item):
    cat = dict()
    cat['id'] = item[0]
    cat['name'] = item[1]
    cat['n_chal'] = item[2]
    cat['disabled'] = item[3]
    return cat

def prepare_chal_json(item):
    chal = dict()
    chal['id'] = item[0]
    chal['name'] = item[1]
    chal['description'] = item[2]
    chal['type'] = item[3]
    chal['trivia'] = item[4]
    return chal

def prepare_user_json(item):
    user = dict()
    user['username'] = item[0]
    user['birthDate'] = item[1]
    user['genre'] = item[2]
    user['challengeWon'] = item[3]
    return user

if __name__ == '__main__':
    app.run()
    ranking(4)