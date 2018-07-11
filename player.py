class Player:

    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.score = 0
        self.challenge_won = 0
        self.win_streak = 0

    def getName(self):
        return self.name

    def getToken(self):
        return self.token

    def getScore(self):
        return self.score

    def getChallengeWon(self):
        return self.challenge_won

    def getWinStrek(self):
        return self.win_streak