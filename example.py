import requests,time

THIS_SERVER = "http://192.168.1.111:5000"

if __name__ == '__main__':
    """requests.post(THIS_SERVER + "/join", json={'username': 'Enzham'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Giangio'})
    time.sleep(2)
    requests.post(THIS_SERVER + "/join", json={'username': 'Syrien'})

    url = THIS_SERVER + "/answer/4/C"
    headers = {'authorization': 'Syrien'}

    r = requests.get(url, headers=headers)
    print(r.text)"""

    json = {"username":"lorry03", "psw": "asdf12345"}
    r = requests.post(THIS_SERVER + "/login", json=json)
    print(r.json())