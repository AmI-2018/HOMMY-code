import requests,time

THIS_SERVER = "http://192.168.1.111:5000"

if __name__ == '__main__':
    requests.post(THIS_SERVER + "/join", json={'username': 'Enzham'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Giangio'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Syrien'})