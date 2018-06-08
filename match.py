from service import randomize
from selenium import webdriver as wd
class Match:
    ONLINE_SERVER = "http://127.0.0.1:5000"
    THIS_SERVER = "http://192.168.1.111:5000"
    MAX_PLAYERS = 8

    driver = wd.Firefox()
    driver.maximize_window()

    players = list()
    score = dict()
    player_queue = list()
    player_turn = list()
    played_chal = list([1,2,3])
    admin = ''
    current_trivia = dict()

    def newPlayer(self, new_player):
        if len(self.players) < self.MAX_PLAYERS:
            self.players.append(new_player)
            self.score[new_player]=0
            return True
        return False

    def setAdmin(self, admin):
        self.admin = str(admin)

    def updateTrivia(self, info):
        self.current_trivia = dict(info)

    def playerTurn(self, number):
        if len(self.players) < number:
            return False
        elif len(self.player_queue) < number:
            self.player_queue = randomize(list(self.players))

        self.player_turn = list()
        for i in range(0,number):
            self.player_turn.append(self.player_queue.pop())


if __name__ == '__main__':
    match = Match()
    match.newPlayer("Enzham")
    match.newPlayer("Syrien")
    match.newPlayer("Giangio")
    match.setAdmin("Enzham")
    match.playerTurn(2)
    print(match.player_queue)
