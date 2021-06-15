from categories import Categories
import pickle
import codecs


class PlayerData:
    def __init__(self, nick="", score=0):
        self.nick = nick
        self.score = score
        self.session_id = ""
        self.categories = Categories()

    def answers_to_pickle(self):
        return codecs.encode(pickle.dumps(self), "base64").decode()

    def show_answers_and_save_score(self, string):
        scoreboard = pickle.loads(codecs.decode(string.encode(), "base64"))
        for s in scoreboard:
            print(s.__str__())
            if s.session_id == str(hash(self.session_id)):
                self.score = s.score
        print("\n")

    def __str__(self) -> str:
        return "Nick: " + self.nick + " Wynik: " + str(self.score) + self.categories.__str__()
