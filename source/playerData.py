
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
        return "Panstwo: "+self.state+" Miasto: "+self.city+" Roslina: "+self.plant+" Zwierze: "+self.animal+" Kolor: "+self.colour+" Imie: "+self.name


