from datetime import datetime
import tkinter as tk
from categories import Categories
import time
import threading


class GUIApp(threading.Thread):
    def __init__(self, host, nick):
        threading.Thread.__init__(self)
        self.start()
        self.created = False
        self.host = host
        self.nick = nick[0:20]
        self.round_time = datetime.now()

    def callback(self):
        self.root.quit()

    def get_values(self):
        values = Categories(state=self.country.get('1.0', 'end').rstrip("\n"),
                            city=self.city.get('1.0', 'end').rstrip("\n"),
                            plant=self.plant.get('1.0', 'end').rstrip("\n"),
                            animal=self.animal.get('1.0', 'end').rstrip("\n"),
                            color=self.color.get('1.0', 'end').rstrip("\n"),
                            name=self.name1.get('1.0', 'end').rstrip("\n"))
        self.clear_fields()
        return values

    def clear_fields(self):
        self.country.delete("1.0", tk.END)
        self.city.delete("1.0", tk.END)
        self.plant.delete("1.0", tk.END)
        self.animal.delete("1.0", tk.END)
        self.color.delete("1.0", tk.END)
        self.name1.delete("1.0", tk.END)

    def clock(self):
        seconds = int((self.round_time - datetime.now()).total_seconds())

        if seconds >= 0:
            self.time.config(text=str(int(seconds/60)).zfill(2) + ":" + str(seconds % 60).zfill(2))
            self.time.after(1000, self.clock)

    def is_created(self):
        return self.created

    def set_time(self, round_time):
        self.round_time = datetime.strptime(round_time, '%Y-%m-%d %H:%M:%S')
        self.clock()

    def set_score(self, score):
        self.score.config(text=score)

    def set_letter(self, letter):
        self.letter.config(text=letter)

    def set_warning(self, warning, color):
        self.warning.config(text=warning, bg=color)

    def start_game(self, letter, round_time):
        self.set_letter(letter)
        self.set_time(round_time)
        self.set_warning("Gra się rozpoczęła! ", "green")

    # def create_room(self, nick, widgets):
    #     self.nick = nick
    #     for w in widgets:
    #         w.place_forget()
    #     self.build_interface()
    #
    # def build_start(self):
    #     self.root = tk.Tk()
    #     self.root.protocol("WM_DELETE_WINDOW", self.callback)
    #     self.root.geometry("690x230")
    #     self.root.resizable(False, False)
    #     self.root.title("Gra \"Państwa-Miasta\"")
    #
    #     widgets = []
    #
    #     title = tk.Label(self.root, text="Państwa-Miasta", font="Verdan 16")
    #     title.place(x=262, y=5)
    #     widgets.append(title)
    #     nick1 = tk.Label(self.root, text="Witaj! Podaj swój nick: ", font="Verdan 10")
    #     nick1.place(x=195, y=65)
    #     widgets.append(nick1)
    #     nick2 = tk.Text(self.root, width=16, height=1)
    #     nick2.place(x=345, y=67)
    #     widgets.append(nick2)
    #     create = tk.Button(text="Załóż pokój", command=lambda: self.create_room(nick2.get('1.0', 'end').rstrip("\n"), widgets))
    #     create.place(x=250, y=120)
    #     widgets.append(create)
    #     join = tk.Button(text="Dołącz do pokoju", command=lambda: self.create_room(nick2.get('1.0', 'end').rstrip("\n"), widgets))
    #     join.place(x=350, y=120)
    #     widgets.append(join)

    def build_interface(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("690x230")
        self.root.resizable(False, False)
        self.root.title("Gra \"Państwa-Miasta\"")

        tk.Label(self.root, text="Pokój gracza: " + self.host, font="Verdan 16").place(x=252, y=5)
        tk.Label(self.root, text="   Witaj " + self.nick + "!", font="Verdan 10").place(x=(66-len(self.nick)*2.8), y=85)
        tk.Label(self.root, text="Twój wynik: ", font="Verdan 10").place(x=57, y=117)
        self.score = tk.Label(self.root, text="0", font="Verdana 10")
        self.score.place(x=128, y=117)
        self.warning = tk.Label(self.root, text="Komunikat!", height=1, width=20, bg="blue")
        self.warning.place(x=31, y=165)

        tk.Label(self.root, text="Litera: ", font="Verdan 11").place(x=310, y=55)
        self.letter = tk.Label(self.root, text="-", font="Verdan 11")
        self.letter.place(x=365, y=55)

        tk.Label(self.root, text="Do końca rundy: ", font="Verdan 11").place(x=430, y=55)
        self.time = tk.Label(self.root, text="00:00", font="Verdan 11")
        self.time.place(x=550, y=55)

        tk.Label(self.root, text="Państwo: ").place(x=220, y=94)
        self.country = tk.Text(self.root, width=16, height=1)
        self.country.place(x=290, y=95)

        tk.Label(self.root, text="Miasto: ").place(x=460, y=94)
        self.city = tk.Text(self.root, width=16, height=1)
        self.city.place(x=520, y=95)

        tk.Label(self.root, text="Kolor: ").place(x=220, y=134)
        self.color = tk.Text(self.root, width=16, height=1)
        self.color.place(x=290, y=135)

        tk.Label(self.root, text="Zwierze: ").place(x=460, y=134)
        self.animal = tk.Text(self.root, width=16, height=1)
        self.animal.place(x=520, y=135)

        tk.Label(self.root, text="Roślina: ").place(x=220, y=174)
        self.plant = tk.Text(self.root, width=16, height=1)
        self.plant.place(x=290, y=175)

        tk.Label(self.root, text="Imię: ").place(x=460, y=174)
        self.name1 = tk.Text(self.root, width=16, height=1)
        self.name1.place(x=520, y=175)

        tk.Label(self.root, text="©PAS Gaming ").place(x=607, y=209)
        self.created = True

    def run(self):
        self.build_interface()
        self.root.mainloop()


# app = App("Host", "Nazwa gracza do 20 znaków")
# time.sleep(1)
# app.set_score(122)
# app.set_letter("S")
# app.set_time("2021-06-10 22:20:00")
# app.set_warning("Gra się rozpoczyna!", "green")
