"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Leaderboard Class (and Score Class) that can load, keep track of, update,
and save the high scores from a game.
"""
from file_functions import log_error
from TextTurtle import TextTurtle
from gui import BOARD_SIZE, INNER_BORDER, OUTER_BORDER, WINDOW_HEIGHT

LEADERBOARD_FILE = "./Logs/leaderboard.log"


class Leaderboard:
    """
    Leaderboard objects are a datastructure of Score objects in ranked order
    that can provide current rankings, add new rankings, and save to a file.
    """
    def __init__(self):
        """Create a new Leaderboard object by reading from the default file"""
        self.leaderboard = []
        self.load_leaderboard()

        # create & write leaderboard heading
        self.leader_heading = TextTurtle(BOARD_SIZE + INNER_BORDER + 10,
                                         OUTER_BORDER * 2 + 10)
        self.leader_heading.write("Leaders:", 22, 'bold')

        # create & write high scores
        self.leaderboard_gui = TextTurtle(BOARD_SIZE + INNER_BORDER + 10, 450)
        self.leaderboard_gui.write(self.print_top_10(), 18)

    def get_leaderboard_length(self):
        """Returns number of items in leaderboard rankings"""
        return len(self.leaderboard)

    def print_top_10(self):
        """
        Represents top 10 entries in leaderboard as string
        for printing to graphics screen
        """
        text_leaderboard = ""
        for i in range(min(10, len(self.leaderboard))):
            text_leaderboard += str(self.leaderboard[i]) + "\n"
        text_leaderboard += ((10 - len(self.leaderboard)) * "\n")
        return text_leaderboard

    def load_leaderboard(self):
        """Reads leaderboard entries from a file"""
        scores = []
        try:
            with open(LEADERBOARD_FILE, mode='r') as in_file:
                for line in in_file:
                    try:
                        score, user = line.strip("\n").split(" : ")
                        scores.append(Score(int(score), user))
                    except ValueError:  # valid scores (if any) will still be read
                        log_error("Leaderboard file contained invalid data")
        except FileNotFoundError:
            log_error("Leaderboard file could not be found")
        self.leaderboard = scores

    def update_leaderboard(self, score, user):
        """Adds a new score to the leaderboard rankings in the appropriate location"""
        new_scoreboard = []
        for i in range(self.get_leaderboard_length()):
            # check new score against each recorded score
            if score < (self.leaderboard[i]).score():  # found place in rankings
                # keep high scores
                for each in self.leaderboard[:i]:
                    new_scoreboard.append(each)
                # insert new score
                new_scoreboard.append(Score(score, user))
                # retain remaining scores
                for each in self.leaderboard[i:]:
                    new_scoreboard.append(each)
                self.leaderboard = new_scoreboard
                self.save_leaderboard()
                self.leaderboard_gui.clear()
                self.leaderboard_gui.write(self.print_top_10(), 18)  # update screen
                return None  # return after inserting new score
        # leaderboard was empty, or new score is more moves than previous largest
        self.leaderboard.append(Score(score, user))
        self.save_leaderboard()
        self.leaderboard_gui.clear()
        self.leaderboard_gui.write(self.print_top_10(), 18)  # update screen

    def save_leaderboard(self):
        """Saves leaderboard rankings to file"""
        with open(LEADERBOARD_FILE, mode='w') as out_file:
            for each in self.leaderboard:
                out_file.write(f"{str(each)}\n")

class Score:
    """
    A Score object containing a player and their score;
    can provide this data in numerical or string formatting
    """
    def __init__(self, score_value, player_name="1UP"):
        """Create a new Score object"""
        self.score_value = score_value
        self.player_name = player_name

    def score(self):
        """Returns the numeric score value"""
        return self.score_value

    def player(self):
        """Returns the player name"""
        return self.player_name

    def __str__(self):
        """Represent a Score object as a string for display or saving"""
        return f"{self.score() : >3} : {self.player()}"
