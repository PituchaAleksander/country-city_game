import time
import tkinter as tk
from categories import Categories

import threading

class App(threading.Thread):

    def __init__(self, nick):
        threading.Thread.__init__(self)
        self.start()
        self.nick = nick

    def callback(self):
        self.root.quit()

    def get_values(self):
        return Categories(state=self.country.get('1.0', 'end'),
                          city=self.city.get('1.0', 'end'),
                          plant=self.plant.get('1.0', 'end'),
                          animal=self.animal.get('1.0', 'end'),
                          color=self.color.get('1.0', 'end'),
                          name=self.name1.get('1.0', 'end'))

    def set_score(self, scores):
        tk.Label(self.root, text=str(scores), font="Verdana 16 bold").grid(row=0, column=6, stick="W")

    def set_letter(self, letter):
        tk.Label(self.root, text=letter, font="Verdana 13 bold").grid(row=5, column=0)

    def build_interface(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        tk.Label(self.root, text="NICK").grid(row=0, column=0)
        tk.Label(self.root, text=self.nick, font="Verdana 16 bold").grid(row=0, column=1, columnspan=3, stick="W")

        tk.Label(self.root, text="SCORES").grid(row=0, column=5, stick="E")
        tk.Label(self.root, text="-", font="Verdana 16 bold").grid(row=0, column=6, stick="W")

        tk.Label(self.root, text="LETTER").grid(row=4, column=0)
        tk.Label(self.root, text="-", font="Verdana 13 bold").grid(row=5, column=0)


        tk.Label(self.root, text="Państwo").grid(row=4, column=1)
        self.country = tk.Text(self.root, width=16, height=2)
        self.country.grid(row=5, column=1)

        tk.Label(self.root, text="Miasto").grid(row=4, column=2)
        self.city = tk.Text(self.root, width=16, height=2)
        self.city.grid(row=5, column=2)

        tk.Label(self.root, text="Roślina").grid(row=4, column=3)
        self.plant = tk.Text(self.root, width=16, height=2)
        self.plant.grid(row=5, column=3)

        tk.Label(self.root, text="Zwierze").grid(row=4, column=4)
        self.animal = tk.Text(self.root, width=16, height=2)
        self.animal.grid(row=5, column=4)

        tk.Label(self.root, text="Kolor").grid(row=4, column=5)
        self.color = tk.Text(self.root, width=16, height=2)
        self.color.grid(row=5, column=5)

        tk.Label(self.root, text="Imię").grid(row=4, column=6)
        self.name1 = tk.Text(self.root, width=16, height=2)
        self.name1.grid(row=5, column=6)

    def run(self):
        self.build_interface()
        self.root.mainloop()

app = App("AMADEUSZ")
time.sleep(6)
app.set_score(12)
app.set_letter("s")
