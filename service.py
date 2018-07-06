import random, time
from threading import Lock
from urllib import request
mutex = Lock()


def homePage(driver, url):
    while True:
        try:
            request.urlopen(url=url)
            break
        except Exception as e:
            print(e)
            time.sleep(1)

    openWebPage(driver,url)

def openWebPage(driver, url):
    global mutex
    mutex.acquire()
    driver.get(url)
    mutex.release()


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
    """a = {'p': 1, 'q': 2}
    b = dict(a)
    print(b)
    a['s']=3
    print(b)
    print(chr(ord('a')+1))"""