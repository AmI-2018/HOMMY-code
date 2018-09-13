import requests, winsound
import service, player, hue, time
THIS_SERVER = "http://192.168.1.188:5000"
SERVER_KEY = "AAAAejrw0Vc:APA91bH-UEiG0Gl9TnLUUjIw44ps3ctL7tYpoEfZ0pqpPqbyo26bgMrmzgZ_wpfs1bGojbezj1qnaYJ3_WmiCZBC" \
             "pkF2QiSfETuc4afOG6E3bllxULSL9qE9nqwcuybaB2whGisOtJeK"
TOKEN = "dUYbTta-Q9Q:APA91bFleC9EbmT3UaWWYV8T4P0aw6fdtLP903c4eXsvpnE9F32g1hncMyIweDHBOutY_Fhn0je4GUcgejfmGFyKLMom6" \
        "h0ezsvwNTePW4K2P1Gr1ovCeJ56tWv7RcoIDgzLbBYRrCg0"
FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"

if __name__ == '__main__':
    res = requests.get("http://192.168.1.102:5000/getRanking/1")
    print(res.json())
    res = requests.get("http://192.168.1.102:5000/getRanking/2")
    print(res.json())
    res = requests.get("http://192.168.1.102:5000/getRanking/3")
    print(res.json())
    res = requests.get("http://192.168.1.102:5000/getRanking/4")
    print(res.json())