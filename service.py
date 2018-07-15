from requests import request, RequestException
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

def randomFrequency():
    ran = random.randint(6,30)
    ran = ran*50
    return ran

def send(method='GET', url=None, data=None, headers={}):
    # the response dictionary, initially empty
    response_dict = dict()

    # check that the URL is not empty
    if url is not None:
        # try to call the URL
        result = None
        try:
            # get the result
            result = request(method, url, data=data, headers=headers)
        except RequestException as e:
            # print the error
            print(e)

        # check result
        if result is not None:
            # consider the response content as JSON and put it in the dictionary
            response_dict = result.json()

    return response_dict


if __name__ == '__main__':
    """a = {'p': 1, 'q': 2}
    b = dict(a)
    print(b)
    a['s']=3
    print(b)
    print(chr(ord('a')+1))"""