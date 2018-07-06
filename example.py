import requests

THIS_SERVER = "http://192.168.1.111:5000"
SERVER_KEY = "AAAAejrw0Vc:APA91bH-UEiG0Gl9TnLUUjIw44ps3ctL7tYpoEfZ0pqpPqbyo26bgMrmzgZ_wpfs1bGojbezj1qnaYJ3_WmiCZBC" \
             "pkF2QiSfETuc4afOG6E3bllxULSL9qE9nqwcuybaB2whGisOtJeK"
TOKEN = "dUYbTta-Q9Q:APA91bFleC9EbmT3UaWWYV8T4P0aw6fdtLP903c4eXsvpnE9F32g1hncMyIweDHBOutY_Fhn0je4GUcgejfmGFyKLMom6" \
        "h0ezsvwNTePW4K2P1Gr1ovCeJ56tWv7RcoIDgzLbBYRrCg0"
FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"
if __name__ == '__main__':
    """requests.post(THIS_SERVER + "/join", json={'username': 'Enzham'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Giangio'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Syrien'})"""

    """url = THIS_SERVER + "/answer/4/D"
    headers = {'authorization': 'Syrien'}

    r = requests.get(url, headers=headers)
    print(r.text)"""
    """print(SERVER_KEY)

    headers = {'Authorization': 'key=' + SERVER_KEY, 'Content-Type': 'application/json'}
    fields = {'to': TOKEN,
              'notification': {
                  'title': 'refresh',
                  'body': 'challenge'
              }
              }
    res = requests.post(FIREBASE_URL, headers=headers, json=fields)"""


    """for i in range(0,4):
        print(requests.get(THIS_SERVER+"/categoriesM"))"""
    res = "ho to save a life"
    res = res.replace(' ', '_')
    print(res)

