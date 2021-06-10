
class Categories:

    def __init__(self, state="", city="", plant="", animal="", color="", name=""):
        self.state = state
        self.city = city
        self.plant = plant
        self.animal = animal
        self.color = color
        self.name = name

    def show(self) -> str:
        return " Panstwo: "+self.state+" Miasto: "+self.city+" Roslina: "+self.plant+" Zwierze: "+self.animal+" Kolor: "+self.color+" Imie: "+self.name

    def calculateScore(self, character, score):
        if len(self.state) > 0 and self.state[0].lower() == character.lower():
            score += 1

        if len(self.city) > 0 and self.city[0].lower() == character.lower():
            score += 1

        if len(self.plant) > 0 and self.plant[0].lower() == character.lower():
            score += 1

        if len(self.animal) > 0 and self.animal[0].lower() == character.lower():
            score += 1

        if len(self.color) > 0 and self.color[0].lower() == character.lower():
            score += 1

        if len(self.name) > 0 and self.name[0].lower() == character.lower():
            score += 1

        return score
