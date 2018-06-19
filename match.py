from service import randomize
from selenium import webdriver as wd
import requests


class Match:
    # CONSTANTS
    ONLINE_SERVER = "http://127.0.0.1:5000"
    THIS_SERVER = "http://192.168.1.111:5000"
    FIREBASE_SERVER_KEY = "AAAAejrw0Vc:APA91bH-UEiG0Gl9TnLUUjIw44ps3ctL7tYpoEfZ0pqpPqbyo26bgMrmzgZ_wpfs1bGojbezj1qna" \
                          "YJ3_WmiCZBCpkF2QiSfETuc4afOG6E3bllxULSL9qE9nqwcuybaB2whGisOtJeK"
    FIREBASE_URL = "https://fcm.googleapis.com/fcm/send"
    MAX_PLAYERS = 8

    # INIT SELENIUM
    driver = wd.Firefox()
    driver.maximize_window()

    # GAME INFO
    players = list()
    tokens = dict()
    score = dict()
    player_queue = list()
    player_turn = list()
    played_chal = list()
    admin = ''
    current_chal = dict()
    current_trivia = dict()
    active = False

    def newPlayer(self, new_player, token):
        if len(self.players) < self.MAX_PLAYERS:
            self.players.append(new_player)
            self.score[new_player] = 0
            self.tokens[new_player] = token
            return True
        return False

    def setAdmin(self, admin):
        self.admin = str(admin)

    def updateTrivia(self, info):
        if info is None:
            self.current_trivia = dict()
        else:
            self.current_trivia = dict(info)

    def updateChallenge(self, challenge):
        self.current_chal = dict(challenge)

    # Choose Randomly who have to play the challenge
    def playerTurn(self, number):
        if len(self.players) < number:
            return False
        elif len(self.player_queue) < number:
            self.player_queue = randomize(list(self.players))

        self.player_turn = list()
        for i in range(0,number):
            self.player_turn.append(self.player_queue.pop())

    def setActive(self, status):
        if (status == True) or (status == False):
            self.active = status

    #Check if an user exist among the current players
    def containsPlayer(self, player):
        tmp = str.lower(player)
        for p in self.players:
            if str.lower(p) == tmp:
                return True
        return False

    # Send a notification to every user (except who clicked the button for the next challenge) in order to update
    # mobile activity
    def sendNotifications(self, exclude_token=""):
        headers = {'Authorization': 'key=' + self.FIREBASE_SERVER_KEY, 'Content-Type': 'application/json'}

        for token in self.tokens:
            if token != exclude_token:
                fields = {'to': self.tokens[token],
                          'notification': {
                              'title': 'refresh',
                              'body': 'challenge'
                            }
                          }
                res = requests.post(self.FIREBASE_URL, headers=headers, json=fields)
                return res

    def getToken(self, player):
        return str(self.tokens[player])

if __name__ == '__main__':
    match = Match()
    """match.newPlayer("Enzham")
    match.newPlayer("Syrien")
    match.newPlayer("Giangio")
    match.setAdmin("Enzham")
    match.playerTurn(2)
    print(match.player_queue)"""
    match.setActive(True)
    print(match.active)
    m2 = Match()
    print(m2.active)
