import pickle
import codecs
from playerData import PlayerData


class Game:
    def __init__(self):
        # self.nick = ""
        # self.score = 0
        self.password = ""          # room password
        self.character = ''
        self.numberOfPlayers = 0
        self.scoreboard = []
        self.answers = PlayerData()
        self.time_end = False

    def writeAnswer(self):
        self.answers.state = ""
        self.answers.city = ""
        self.answers.plant = ""
        self.answers.animal = ""
        self.answers.color = ""
        self.answers.name = ""

        print("Podaj odpowiednia liczbę aby wybrać opcje:\n1:państwo\n2:miasto\n3:roslina\n4:zwierze\n5:kolor\n6:imie\n7:wyświetl wynik i odpowiedzi\n8:zakończ\nLitera: "+self.character)
        while not self.time_end:
            x = int(input("Podaj liczbe: "))
            if x == 1:
                self.answers.state = input("Podaj państwo: ")
            elif x == 2:
                self.answers.city = input("Podaj miasto: ")
            elif x == 3:
                self.answers.plant = input("Podaj rosline: ")
            elif x == 4:
                self.answers.animal = input("Podaj zwierze: ")
            elif x == 5:
                self.answers.color = input("Podaj kolor: ")
            elif x == 6:
                self.answers.name = input("Podaj imie: ")
            elif x == 7:
                print(self.answers.show())
            elif x == 8:
                break

    def answersToPickle(self):
        return codecs.encode(pickle.dumps(self.answers), "base64").decode()

    def showScoreAndAnswers(self):
        print(len(self.scoreboard))
        for s in self.scoreboard:
            print(s.show())
            if s.nick == self.answers.nick:
                self.answers.score = s.score

    def pickleToScoreBoard(self, string):
        self.scoreboard = pickle.loads(codecs.decode(string.encode(), "base64"))

# ===================client-host===================

    def calculateResults(self):
        for s in self.scoreboard:
            s.calculateScore(self.character)

    def scoreBoardtoPickle(self):
        return codecs.encode(pickle.dumps(self.scoreboard), "base64").decode()


    def addAnswers(self, string):
        score = pickle.loads(codecs.decode(string.encode(), "base64"))
        self.scoreboard.append(score)