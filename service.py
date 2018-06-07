from selenium import webdriver as wd
import random
driver = wd.Firefox()
THIS_SERVER = "http://192.168.1.111:5000"


def categories():
    driver.get(THIS_SERVER + "/categories")


def challenge(chal_id):
    driver.get(THIS_SERVER + "/viewChallenge/" + chal_id)


def players():
    driver.get(THIS_SERVER + "/players")


def endGame():
    driver.get(THIS_SERVER + "/endgame")


def randomize(lista):
    new_list = list()
    i = 0
    length = len(lista)
    while i < length:
        i = i+1
        ran = random.randint(0,length-i)
        new_list.append(lista[ran])
        lista.pop(ran)

    return new_list

if __name__ == '__main__':
    a = {'p': 1, 'q': 2}
    b = dict(a)
    print(b)
    a['s']=3
    print(b)