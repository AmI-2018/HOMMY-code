import requests, winsound
import service, player, hue, time, operator
THIS_SERVER = "http://192.168.1.111:5000"
SERVER_KEY = "AAAAejrw0Vc:APA91bH-UEiG0Gl9TnLUUjIw44ps3ctL7tYpoEfZ0pqpPqbyo26bgMrmzgZ_wpfs1bGojbezj1qnaYJ3_WmiCZBC" \
             "pkF2QiSfETuc4afOG6E3bllxULSL9qE9nqwcuybaB2whGisOtJeK"
TOKEN = "dUYbTta-Q9Q:APA91bFleC9EbmT3UaWWYV8T4P0aw6fdtLP903c4eXsvpnE9F32g1hncMyIweDHBOutY_Fhn0je4GUcgejfmGFyKLMom6" \
        "h0ezsvwNTePW4K2P1Gr1ovCeJ56tWv7RcoIDgzLbBYRrCg0"
FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"

if __name__ == '__main__':
    # winsound.Beep(350, 5000)
    """player = vlc.MediaPlayer("static/music trivia/payday.mp3")
    player.play()"""
    json = {"username": "lorry03", "chal_id": 3, "score": 600}
    res = requests.post(THIS_SERVER+ "/updateBestScore", json=json)
    print(res.json())
