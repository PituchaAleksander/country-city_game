import pickle
import codecs
from playerData import PlayerData


class GameData:
    def __init__(self):
        self.password = ""          # room password
        self.character = ''
        self.numberOfPlayers = 0
        self.scoreboard = []

# ===================client-host===================

    def calculateResults(self):
        for s in self.scoreboard:
            s.score=s.categories.calculateScore(self.character, s.score)

    def scoreBoardtoPickle(self):
        return codecs.encode(pickle.dumps(self.scoreboard), "base64").decode()


    def addAnswers(self, string):
        score = pickle.loads(codecs.decode(string.encode(), "base64"))
        self.scoreboard.append(score)