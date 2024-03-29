class Player:

    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.current_score = 0
        self.score = 0
        self.challenge_won = 0
        self.correct_answer = 0

    def getName(self):
        return self.name

    def getToken(self):
        return self.token

    def getScore(self):
        return self.score

    def getCurrentScore(self):
        return self.current_score

    def getChallengeWon(self):
        return self.challenge_won

    def getWinStrek(self):
        return self.win_streak

    def addPoints(self, points, id=-1):
        if id == 4:
            self.correct_answer = self.correct_answer + 1
            multiplier = 1
            if self.correct_answer % 4 == 0:
                multiplier = 1 + int(self.correct_answer / 3)
            self.current_score = self.current_score + points * multiplier
        else:
            self.current_score = self.current_score + points

    def updateScore(self):
        self.score = self.score + self.current_score
        self.current_score = 0

    def resetCorrectAnswer(self):
        self.correct_answer = 0

    def win(self):
        self.challenge_won = self.challenge_won + 1
