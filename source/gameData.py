import pickle
import codecs

class GameData:
    def __init__(self):
        self.password = ""          # room password
        self.letter = ''
        self.numberOfPlayers = 0
        self.scoreboard = []

    def set_letter(self, letter):
        self.letter = str(letter).upper()

    def calculate_results(self):
        for s in self.scoreboard:
            s.score = s.categories.calculate_score(self.letter, s.score)

    def score_board_to_pickle(self):
        return codecs.encode(pickle.dumps(self.scoreboard), "base64").decode()

    def add_answers(self, string):
        score = pickle.loads(codecs.decode(string.encode(), "base64"))
        self.scoreboard.append(score)
