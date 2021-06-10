import pickle
import codecs
from playerData import PlayerData


class GameData:
    def __init__(self):
        self.password = ""          # room password
        self.letter = ''
        self.numberOfPlayers = 0
        self.scoreboard = []

    def set_letter(self, letter):
        self.letter = str(letter).upper()

    def calculateResults(self):
        for s in self.scoreboard:
            s.score = s.categories.calculateScore(self.letter, s.score)

    def scoreBoardtoPickle(self):
        return codecs.encode(pickle.dumps(self.scoreboard), "base64").decode()

    def addAnswers(self, string):
        score = pickle.loads(codecs.decode(string.encode(), "base64"))
        self.scoreboard.append(score)
