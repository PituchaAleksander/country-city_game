
class PlayerData:

    def __init__(self, nick="", score=0, state="", city="", plant="", animal="", color="", name=""):
        self.nick = nick
        self.score = score
        self.state = state
        self.city = city
        self.plant = plant
        self.animal = animal
        self.color = color
        self.name = name

    def show(self) -> str:
        return "Nick: "+self.nick+" Wynik: "+str(self.score)+" Panstwo: "+self.state+" Miasto: "+self.city+" Roslina: "+self.plant+" Zwierze: "+self.animal+" Kolor: "+self.color+" Imie: "+self.name

    def calculateScore(self, character):
        if len(self.state) > 0 and self.state[0] == character:
            self.score += 1

        if len(self.city) > 0 and self.city[0] == character:
            self.score += 1

        if len(self.plant) > 0 and self.plant[0] == character:
            self.score += 1

        if len(self.animal) > 0 and self.animal[0] == character:
            self.score += 1

        if len(self.color) > 0 and self.color[0] == character:
            self.score += 1

        if len(self.name) > 0 and self.name[0] == character:
            self.score += 1