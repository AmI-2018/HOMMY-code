from selenium import webdriver as wd
import requests, threading, service as srv, player


class Match:
    # CONSTANTS
    ONLINE_SERVER = "http://127.0.0.1:5000"
    THIS_SERVER = "http://192.168.1.111:5000"
    FIREBASE_SERVER_KEY = "AAAAejrw0Vc:APA91bH-UEiG0Gl9TnLUUjIw44ps3ctL7tYpoEfZ0pqpPqbyo26bgMrmzgZ_wpfs1bGojbezj1qna" \
                          "YJ3_WmiCZBCpkF2QiSfETuc4afOG6E3bllxULSL9qE9nqwcuybaB2whGisOtJeK"
    FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"
    MAX_PLAYERS = 8

    # GAME INFO
    players = dict()
    player_queue = list()
    player_turn = list()
    played_chal = list([4,2,3])
    number_played_challenge = 0
    quiz = list()
    admin = ''
    current_categ = ""
    current_chal = dict()
    current_trivia = dict()
    active = False
    voice_hz = dict()

    def __init__(self):
        # INIT SELENIUM
        self.driver = wd.Firefox()
        self.driver.maximize_window()
        threading.Thread(target=srv.homePage, args=(self.driver, self.THIS_SERVER)).start()

    def newPlayer(self, new_player, token):
        if len(self.players) < self.MAX_PLAYERS:
            p = player.Player(new_player,token)
            self.players[new_player] = p
            return True
        return False

    def setAdmin(self, admin):
        self.admin = str(admin)

    def updateTrivia(self, info):
        if info is None:
            self.current_trivia = dict()
            self.quiz = list()
        else:
            self.current_trivia = dict(info)
            self.quiz.append(info['q_id'])

    def updateChallenge(self, challenge):
        self.current_chal = dict(challenge)
        self.current_chal['active'] = False
        self.number_played_challenge = self.number_played_challenge + 1

    # Choose Randomly who have to play the challenge
    def playerTurn(self, number):
        flag = 1
        if len(self.players) < number:
            return False
        elif len(self.player_queue) < number:
            self.player_queue = srv.randomize(self.getPlayersName())
            flag = -1

        self.player_turn = list()
        for i in range(0,number):
            self.player_turn.append(self.player_queue.pop())

        return flag

    def setActiveMatch(self, status):
        if (status is True) or (status is False):
            self.active = status

    # Check if an user exist among the current players
    def containsPlayer(self, player):
        tmp = str.lower(player)
        for p in self.players:
            if str.lower(self.players[p].getName()) == tmp:
                return True
        return False

    # Send a notification to every user (except who clicked the button for the next challenge) in order to update
    # mobile activity
    def sendNotifications(self, players=list()):
        all = False
        if len(players) == 0:
            all = True

        headers = {'Authorization': 'key=' + self.FIREBASE_SERVER_KEY, 'Content-Type': 'application/json'}
        res = list()
        if all:
            for p in self.players:
                fields = {'to': self.players[p].getToken(),
                          'notification': {
                              'title': 'refresh',
                              'body': 'challenge'
                            }
                          }
                res.append(requests.post(self.FIREBASE_URL, headers=headers, json=fields).text)
        else:
            for p in players:
                fields = {'to': self.players[p].getToken(),
                          'notification': {
                              'title': 'refresh',
                              'body': 'challenge'
                            }
                          }
                res.append(requests.post(self.FIREBASE_URL, headers=headers, json=fields).text)
        return res

    def getToken(self, player):
        return str(self.players[player].getToken())

    def setCategory(self, category):
        self.current_categ = category

    def getCategory(self):
        return self.current_categ

    def isActive(self, dictionary):
        return dictionary['active']

    def setActive(self, dictionary, bool):
        dictionary['active'] = bool

    def voiceHzResult(self, user, given_frequency):
        self.voice_hz[user] = given_frequency

    def getVoiceHzResult(self, key):
        if key in self.voice_hz:
            return self.voice_hz[key]
        return -1

    def getPlayersName(self):
        """players = list()
        for p in self.players:
            players.append(self.players[p].getName())"""
        return list(self.players)

    def getCurrentIdChal(self):
        if "id" in self.current_chal:
            return self.current_chal['id']
        return -1

    def getPlayer(self, name):
        return self.players[name]


if __name__ == '__main__':
    match = Match()
    """match.newPlayer("Enzham")
    match.newPlayer("Syrien")
    match.newPlayer("Giangio")
    match.setAdmin("Enzham")
    match.playerTurn(2)
    print(match.player_queue)"""
    match.setActive(True)
    match.newPlayer("lorry03", "token")
    match.newPlayer("syrien95", "token")
