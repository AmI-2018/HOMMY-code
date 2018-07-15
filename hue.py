import service

#base_URL = 'http://192.168.0.201' #URL of the bridge

base_URL = 'http://localhost:8000' #emulator URL

#username = 'jhfahslfhalsflaj' #username fisico

username = 'newdeveloper'

lights_URL = base_URL + '/api/' + username + '/lights/'

all_the_lights = service.send(url=lights_URL)

def base():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 46920, "sat" : 254, "effect" : "colorloop" }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def fitness():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 12750 }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def voice():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 46920 }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def dance():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 12750, "effect" : "colorloop" }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def wrong():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 0 }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def right():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : true, "hue": 25500 }'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1

def off():
    for light in all_the_lights:
        url_to_call = lights_URL + light + '/state'
        body = '{ "on" : false}'
        service.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})
    return 1