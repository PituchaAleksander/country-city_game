import json
from playerData import playerData

class game:

    def __init__(self):
        self.nick=""
        self.score = 0
        self.character=''
        self.numberOfPlayers=0
        self.scoreboard=[]

    def writeAnswer(self):
        answers = playerData()
        answers.nick=self.nick
        answers.score=self.score

        print("Podaj odpowiednia liczbę aby wybrać opcje:\n1:państwo\n2:miasto\n3:roslina\n4:zwierze\n5:kolor\n6:imie\n7:wyświetl odpowiedzi\n8:zakończ")
        while True:
            x=int(input("Podaj liczbe: "))
            if x==1:
                answers.state = input("Podaj państwo: ")
            elif x==2:
                answers.city = input("Podaj miasto: ")
            elif x==3:
                answers.plant = input("Podaj rosline: ")
            elif x == 4:
                answers.animal = input("Podaj zwierze: ")
            elif x==5:
                answers.colour = input("Podaj kolor: ")
            elif x==6:
                answers.name = input("Podaj imie: ")
            elif x==7:
                print(answers.show())
            elif x==8:
                break
            self.ans=answers

        return json.dumps(answers.__dict__)

    def showScoreAndAnswers(self):
        for i in range(0, self.numberOfPlayers):
            print(self.scoreboard[i].show())
            if self.scoreboard[i].nick==self.nick:
                self.score=self.scoreboard[i].score

    def calculateResults(self):

        for i in range(0, self.numberOfPlayers):
            self.scoreboard[i].calculateScore(self.character)
        print("Podaje wynik")

    def getSocreBoardtoJson(self):
        print("Zwracam Jsona")
        json_string = json.dumps(self.scoreboard, default=obj_dict)

        return json_string

    def setSocreBoard(self):

        print("Ustawiam tablice wyników")

def obj_dict(obj):
    return obj.__dict__

g=game()
print(g.writeAnswer())
print(g.getJson())

