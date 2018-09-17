import service, time

base_URL = 'http://192.168.0.201' #URL of the bridge

#base_URL = 'http://localhost:8000' #emulator URL

username = 'byJxxNNsW5pkEi-yNr3kbt5YOqyIcRspdUi2VLBI' #username fisico

#username = 'newdeveloper'

lights_URL = base_URL + '/api/' + username + '/lights/'
id1 = 12
id2 = 9
LOOP = False

all_the_lights=""
def init():
    global all_the_lights
    all_the_lights = service.send(url=lights_URL)
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 0, "sat" : 254, "bri": 0, "effect" : "none" }'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
def base():
    global LOOP
    LOOP = True
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 0, "sat" : 254,"bri": 254, "effect" : "colorloop" }'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def fitness():
    global LOOP
    if LOOP:
        init()
        LOOP = False
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 12750,"bri": 254 }'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def voice():
    global LOOP
    if LOOP:
        init()
        LOOP = False
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 46920, "sat" : 254,"bri": 254, "effect": "none" }'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def dance():
    global LOOP
    LOOP = True
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 12750,"bri": 254, "effect" : "colorloop" }'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def wrong():
    global LOOP
    if LOOP:
        init()
        LOOP = False
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 0 ,"bri": 254, "effect" : "none"}'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def right():
    global LOOP
    if LOOP:
        init()
        LOOP = False
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : true, "hue": 25500,"bri": 254, "effect" : "none" }'
            res = service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return res

def off():
    for light in all_the_lights:
        if (int(light) == id1) or (int(light) == id2):
            url_to_call = lights_URL + light + '/state'
            body = '{ "on" : false}'
            service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1


if __name__ == '__main__':
    init()
    print(all_the_lights)
    base()

    time.sleep(3)
    wrong()
