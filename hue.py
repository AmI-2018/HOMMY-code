import hueApi,time

#base_URL = 'http://192.168.0.201' #URL of the bridge

base_URL = 'http://localhost:8000' #emulator URL

#username = 'jhfahslfhalsflaj' #username fisico

username = 'newdeveloper'

lights_URL = base_URL + '/api/' + username + '/lights/'

all_the_lights = hueApi.send(url=lights_URL)

def base():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 46920, "sat" : 254, "effect" : "colorloop" }'
        hueApi.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def wrong():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 0 }'
        hueApi.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def right():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 25500 }'
        hueApi.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def off():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : false}'
        hueApi.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1