"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Gameboard Class is the primary class of the Tile Swap Game. It creates/contains a screen,
TileSet object, Leaderboard object, LoadMenu object that stores and can toggle between
all accessible valid puzzles, and all other GUI elements including Button objects
for user input and text objects for printing information.  It also handles all click
events, and instructs each of its elements to do update if clicked upon.
"""
from gui import *
from LoadMenu import *
from Leaderboard import *
from TileSet import TileSet
from TextTurtle import TextTurtle
from Button import create_gui_buttons

DEFAULT_PUZZLE = "mario.puz"


class Gameboard:
    """
    The Gameboard class contains all elements of the Tile Game, including its GUI,
    data structures, objects, user interaction/mouseclick handling, and operation
    """
    def __init__(self, player_name="1UP", moves_to_win=50):
        """
        Creates a new Gameboard with a screen, GUI Leaderboard, score counter,
        LoadMenu (for when needed), and (default) TileSet, and shuffles the
        tileset to start the game
        """
        # initialize variables
        self.player_name = player_name
        self.moves_to_win = moves_to_win
        self.game_over = False
        self.clicked = False

        # create window
        self.screen = setup_main_screen()

        # create leaderboard and move counter
        self.leaderboard = Leaderboard()
        self.move_counter = TextTurtle(OUTER_BORDER + 20,
                                       WINDOW_HEIGHT - OUTER_BORDER - 35, "black")
        self.move_counter.write_score(0, self.moves_to_win)

        # create puzzle load menu; load default puzzle; create default tileset
        self.menu = LoadMenu()
        self.puzzle_data = load_puzzle(DEFAULT_PUZZLE)
        if self.puzzle_data is not False:
            self.tileset = TileSet(self.puzzle_data)
        else:  # default puzzle is somehow missing; log error and close
            log_error("Critical error loading default puzzle", print_to_console=True)
            quit_game()
            raise FileNotFoundError

        # create buttons
        self.button_reset, self.button_load_other, \
            self.button_load, self.button_quit = create_gui_buttons()

        # create status/warning popups; hide initially
        self.popup_too_many_files, self.popup_leaderboard_err, \
            self.popup_game_status = create_popups()
        if self.leaderboard.get_leaderboard_length() != 0:
            self.popup_leaderboard_err.hide()

        # shuffle tiles and start game
        turtle.tracer(True)
        self.tileset.shuffle()  # For intense shuffle: (speed=0, swaps=1000, trace=False)
        self.screen.onclick(self.register_click)

    def already_clicked(self, boolean=None):
        """
        Checks whether a click was already logged
        :param boolean: if provided, records boolean as new "clicked" state
        :return: whether a click was previously logged
        """
        if boolean is not None:
            self.clicked = boolean
        return self.clicked

    def register_click(self, x, y):
        """
        Checks each object on the screen to determine if a click was upon it.
        If an object was clicked, perform appropriate actions:
         > Buttons trigger appropriate actions at appropriate times
         > If Menu is open, allow Menu selections
         > If Menu is closed and game is not over, allow Tile actions
        """
        # avoid registering multiple clicks simultaneously
        if self.already_clicked():
            return None
        self.already_clicked(True)
        # check screen objects for clicks
        self.button_load.register_click(x, y)
        self.button_quit.register_click(x, y)
        # load puzzle menu is shown; check for selection of a thumbnail
        if self.menu.show_menu():
            self.menu.register_click(x, y)
            self.button_load_other.register_click(x, y)
            self.check_menu_selection()
            # user selected to manually enter a filename
            if self.button_load_other.state():
                self.button_load_other.state(False)
                self.load_file_manually()
        # only allow game moves or game resets if not in load menu
        elif not self.game_over:
            self.tileset.register_click(x, y)  # check if tile was clicked
            self.button_reset.register_click(x, y)  # check if reset button was clicked
            # if running out of moves, change move counter to red
            if self.tileset.move_count() + 10 >= self.moves_to_win:
                self.move_counter.change_color("red")
            # update score
            self.move_counter.write_score(self.tileset.move_count(), self.moves_to_win)
            # check for victory
            if self.tileset.victory_achieved():
                self.victory()
                # turtle.ontimer(quit_game, 3000)
            # check for loss
            elif self.tileset.move_count() >= self.moves_to_win:
                # show loss message
                self.popup_game_status.change_image("Resources/Lose.gif")
                self.popup_game_status.show()
                self.game_over = True
                # turtle.ontimer(quit_game, 3000)
        # if reset button is pressed
        if self.button_reset.state():
            self.tileset.unscramble()  # tell tileset to unscramble itself
            self.button_reset.state(False)  # reset button state to unpressed
        # if load button is pressed
        if self.button_load.state():
            self.open_load_menu()
        # if quit button is pressed
        if self.button_quit.state():
            self.popup_game_status.change_image("Resources/quitmsg.gif")
            self.popup_game_status.show()
            turtle.ontimer(quit_game, 2000)
        self.already_clicked(False)  # click resolved: allow registering new clicks

    def victory(self):
        """Display victory message; update leaderboard; set game_over to True"""
        # show victory message
        self.popup_game_status.change_image("Resources/winner.gif")
        self.popup_game_status.show()
        # add score to leaderboard
        self.leaderboard.update_leaderboard(self.tileset.move_count(), self.player_name)
        self.game_over = True

    def open_load_menu(self):
        """Dismiss the tileset and show the 'load puzzle' menu"""
        self.tileset.reset()  # dismiss tileset
        self.button_reset.hide()  # hide reset button (it's useless)
        self.button_load_other.show()  # replace reset button with load-by-filename button
        self.popup_game_status.hide()
        self.move_counter.clear()
        self.button_load.state(False)  # reset load button state to unpressed
        self.menu.show_menu(True)  # show load menu
        if self.menu.too_many():  # if more than 9 files are found, show notification
            self.popup_too_many_files.show()

    def check_menu_selection(self):
        """
        Check if a puzzle thumbnail was clicked on; if so,
        load the corresponding puzzle and close the menu
        """
        if self.menu.selection() is not None:
            # load new puzzle; replace tiles with new tileset
            self.puzzle_data = self.menu.selected_puzzle_data()
            self.tileset = TileSet(self.puzzle_data)
            self.close_menu()

    def load_file_manually(self):
        """Allows a user to enter a puzzle filename manually to try to load it"""
        file_to_load = turtle.textinput("Load Other File", "Enter filename:")
        loaded_file = load_puzzle(file_to_load)
        if loaded_file is not False:
            self.puzzle_data = loaded_file
            self.tileset = TileSet(self.puzzle_data)
            self.close_menu()
        else:
            self.popup_leaderboard_err.change_image("Resources/file_error.gif")
            self.popup_leaderboard_err.show()

    def close_menu(self):
        """
        Hide menu; update buttons and status readouts for gameplay; shuffle new TileSet
        """
        # hide menu; return to gameplay
        self.menu.show_menu(False)
        self.menu.reset_selection()
        self.button_load_other.hide()
        self.button_reset.show()
        self.popup_too_many_files.hide()
        self.popup_leaderboard_err.hide()
        # reset move counter
        self.move_counter.reset_color()
        self.move_counter.write_score(self.tileset.move_count(), self.moves_to_win)
        # shuffle tiles & begin game
        turtle.tracer(True)
        self.tileset.shuffle()
        self.game_over = False


def quit_game():
    """Display the closing credits for several seconds before ending the program"""
    turtle.clearscreen()
    SplashScreen("Resources/credits.gif", 460, 430)
    turtle.ontimer(turtle.bye, 3000)
