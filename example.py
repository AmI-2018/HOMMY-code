import requests, webbrowser

THIS_SERVER = "http://192.168.1.111:5000"
PROVA = "http://127.0.0.1:5000/join"
if __name__ == '__main__':
    #requests.post(THIS_SERVER + "/join", json={'username': 'asd'})
    requests.post(PROVA, json={'username': 'asd'})
    #webbrowser.open(THIS_SERVER + "/players")