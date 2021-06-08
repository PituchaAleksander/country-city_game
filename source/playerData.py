
class playerData:

    def __init__(self):
        self.nick=""
        self.score=0
        self.state = ""
        self.city = ""
        self.plant=""
        self.animal = ""
        self.colour = ""
        self.name = ""

    def show(self) -> str:
        return "Nick: "+self.nick+" Wynik: "+str(self.score)+"Panstwo: "+self.state+" Miasto: "+self.city+" Roslina: "+self.plant+" Zwierze: "+self.animal+" Kolor: "+self.colour+" Imie: "+self.name

    def calculateScore(self, character):
        if len(self.state)>0 and self.state[0]==character:
            self.score+=1

        if len(self.city)>0 and self.city[0]==character:
            self.score+=1

        if len(self.plant)>0 and self.plant[0]==character:
            self.score+=1

        if len(self.animal)>0 and self.animal[0]==character:
            self.score+=1

        if len(self.colour)>0 and self.colour[0]==character:
            self.score+=1

        if len(self.name)>0 and self.name[0]==character:
            self.score+=1

