from flask import Flask, render_template, url_for, redirect, jsonify
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

@app.route('/getChallenge/<category>', methods=['GET'])
def getChallenge(category):
    res = db.getChallenge(category)
    chal = []

    res = prepare_chal_json(res)
    chal.append(res)
    return jsonify({'challenges': chal})

@app.route('/getChallenge/<int:id>', methods=['GET'])
def getChallenge2(id):
    res = db.getChallenge2(id)
    chal = []

    res = prepare_chal_json(res)
    chal.append(res)
    return jsonify({'challenges': chal})

def prepare_cat_json(item):
    cat = dict()
    cat['name'] = item[0]
    cat['n_chal'] = item[1]
    return cat

def prepare_chal_json(item):
    chal = dict()
    chal['id'] = item[0]
    chal['name'] = item[1]
    chal['description'] = item[2]
    chal['type'] = item[3]
    return chal

    return cat

if __name__ == '__main__':
    app.run()
