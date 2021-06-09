import json
from playerData import PlayerData


class Game:

    def __init__(self):
        # self.nick = ""
        # self.score = 0
        self.character = ''
        self.numberOfPlayers = 0
        self.scoreboard = []
        self.answers = PlayerData()
        self.time_end = False

    def writeAnswer(self):
        self.answers = PlayerData()
        self.answers.state = ""
        self.answers.city = ""
        self.answers.plant = ""
        self.answers.animal = ""
        self.answers.color = ""
        self.answers.name = ""

        print("Podaj odpowiednia liczbę aby wybrać opcje:\n1:państwo\n2:miasto\n3:roslina\n4:zwierze\n5:kolor\n6:imie\n7:wyświetl wynik i odpowiedzi\n8:zakończ")
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

    def answersToJson(self):
        return json.dumps(self.answers.__dict__)

    def showScoreAndAnswers(self):
        for i in range(0, self.numberOfPlayers):
            print(self.scoreboard[i].show())
            if self.scoreboard[i].nick == self.nick:
                self.score = self.scoreboard[i].score

    def jsonToScoreBoard(self, json_string):
        scoreboard = json.loads(json_string, object_hook=decode_playerData)
        for i in range(0, len(scoreboard)):
            self.addAnswers(scoreboard[i])

# ===================client-host===================

    def calculateResults(self):
        for i in range(0, self.numberOfPlayers):
            self.scoreboard[i].calculateScore(self.character)
        print("Podaje wynik")

    def getScoreBoardtoJson(self):
        print("Zwracam Jsona")
        return json.dumps(self.scoreboard, default=obj_dict)

    def addAnswers(self, json_string):
        print("Dodaje do tablicy wyników")
        score = json.loads(json_string, object_hook=decode_playerData)
        self.scoreboard.append(score)

def obj_dict(obj):
    return obj.__dict__

def decode_playerData(json):
    return PlayerData(json['nick'], json['score'], json['state'], json['city'], json['plant'], json['animal'], json['color'], json['name'])



