import tkinter as tk
from playerData import PlayerData

import threading

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def get_values(self):
        return PlayerData(state=self.country.get('1.0', 'end'),
                          city=self.city.get('1.0', 'end'),
                          plant=self.plant.get('1.0', 'end'),
                          animal=self.animal.get('1.0', 'end'),
                          color=self.color.get('1.0', 'end'),
                          name=self.name1.get('1.0', 'end'))

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        tk.Label(self.root, text="Państwo").grid(row=0, column=0)
        self.country = tk.Text(self.root, width=16, height=2)
        self.country.grid(row=1, column=0)

        tk.Label(self.root, text="Miasto").grid(row=0, column=1)
        self.city = tk.Text(self.root, width=16, height=2)
        self.city.grid(row=1, column=1)

        tk.Label(self.root, text="Roślina").grid(row=0, column=2)
        self.plant = tk.Text(self.root, width=16, height=2)
        self.plant.grid(row=1, column=2)

        tk.Label(self.root, text="Zwierze").grid(row=0, column=3)
        self.animal = tk.Text(self.root, width=16, height=2)
        self.animal.grid(row=1, column=3)

        tk.Label(self.root, text="Kolor").grid(row=0, column=4)
        self.color = tk.Text(self.root, width=16, height=2)
        self.color.grid(row=1, column=4)

        tk.Label(self.root, text="Imię").grid(row=0, column=5)
        self.name1 = tk.Text(self.root, width=16, height=2)
        self.name1.grid(row=1, column=5)

        self.root.mainloop()



# class Application(tk.Frame):
#     def __init__(self):
#         root = tk.Tk()
#         root.resizable(width=False, height=False)
#         super().__init__(root)
#         self.master = root
#         self.grid(padx=10, pady=10)
#         self.create_widgets()
#
#     def create_widgets(self):
#         tk.Label(self, text="Państwo").grid(row=0, column=0)
#         self.country = tk.Text(self, width=16, height=2)
#         self.country.grid(row=1, column=0)
#
#         tk.Label(self, text="Miasto").grid(row=0, column=1)
#         self.city = tk.Text(self, width=16, height=2)
#         self.city.grid(row=1, column=1)
#
#         tk.Label(self, text="Roślina").grid(row=0, column=2)
#         self.plant = tk.Text(self, width=16, height=2)
#         self.plant.grid(row=1, column=2)
#
#         tk.Label(self, text="Zwierze").grid(row=0, column=3)
#         self.animal = tk.Text(self, width=16, height=2)
#         self.animal.grid(row=1, column=3)
#
#         tk.Label(self, text="Kolor").grid(row=0, column=4)
#         self.color = tk.Text(self, width=16, height=2)
#         self.color.grid(row=1, column=4)
#
#         tk.Label(self, text="Imię").grid(row=0, column=5)
#         self.name = tk.Text(self, width=16, height=2)
#         self.name.grid(row=1, column=5)

        # self.log = tk.Text(self, state="disable", width=80, height=32)
        # self.log.grid(row=2, column=0)

        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.pack(side="bottom")

    # def get_values(self):
    #     return PlayerData(state=self.country.get('1.0', 'end'),
    #                       city=self.city.get('1.0', 'end'),
    #                       plant=self.plant.get('1.0', 'end'),
    #                       animal=self.animal.get('1.0', 'end'),
    #                       color=self.color.get('1.0', 'end'),
    #                       name=self.name.get('1.0', 'end'))
    #
    #
    # def say_hi(self):
    #     self.country['state'] = 'disable'
    #     print(self.country.get('1.0', 'end'))


# root = tk.Tk()
# root.resizable(width=False, height=False)
# app = Application(master=root)
# app.mainloop()
