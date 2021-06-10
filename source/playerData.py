from categories import Categories
import pickle
import codecs

class PlayerData:

    def __init__(self, nick="", score=0):
        self.nick = nick
        self.score = score
        self.categories = Categories()

    def answersToPickle(self):
        return codecs.encode(pickle.dumps(self), "base64").decode()

    def showScoreAndAnswers(self, string):
        scoreboard = pickle.loads(codecs.decode(string.encode(), "base64"))
        for s in scoreboard:
            print(s.show())
            if s.nick == self.nick:
                self.score = s.score

    def show(self) -> str:
        return "Nick: "+self.nick+" Wynik: "+str(self.score) + self.categories.show()