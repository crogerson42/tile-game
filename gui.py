"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Contains GUI elements of the tile game including:
    > Constants: Screen size constants
    > Functions: Screen setup functions
    > Class: Rectangle for use as a GUI element
    > Class: Splash Screen for use when opening/closing the game
"""
import turtle
from ImageTurtle import ImageTurtle

# GUI constants
WINDOW_WIDTH = 825  # 825
WINDOW_HEIGHT = 675  # 675

BOARD_SIZE = 505  # 505
OUTER_BORDER = 40  # 40
INNER_BORDER = 30  # 30

DEFAULT_TILE_GAP = 10  # 10
DEFAULT_TILE_BORDER = 105  # 105

BUTTON_SPACING = 100  # 100
BUTTON_X_RIGHT = WINDOW_WIDTH - OUTER_BORDER + 40
BUTTON_Y = (BOARD_SIZE + INNER_BORDER + WINDOW_HEIGHT - OUTER_BORDER) // 2

THUMBNAIL_X = WINDOW_WIDTH - OUTER_BORDER - 53  # 707
THUMBNAIL_Y = OUTER_BORDER + 33  # 73

WINDOW_NAME = "CS5001 Sliding Puzzle Game"


def setup_main_screen():
    """Returns a turtle Screen object set up for use in the game"""
    screen = turtle.Screen()
    turtle.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    turtle.setworldcoordinates(0, WINDOW_HEIGHT, WINDOW_WIDTH, 0)
    turtle.title(WINDOW_NAME)
    turtle.tracer(False)
    draw_gui_outlines()
    return screen


def create_popups():
    """
    Create default status popup objects
    :return: popup_too_many_files, popup_leaderboard_err, popup_game_status
    """
    popup_too_many_files = ImageTurtle("Resources/file_warning_9.gif",
                                       BUTTON_X_RIGHT - 5 * BUTTON_SPACING, BUTTON_Y)
    popup_leaderboard_err = ImageTurtle("Resources/leaderboard_error.gif",
                                        (BOARD_SIZE + INNER_BORDER + WINDOW_WIDTH -
                                         OUTER_BORDER) / 2, BOARD_SIZE - 50)
    popup_game_status = ImageTurtle("Resources/winner.gif",
                                    (BOARD_SIZE + OUTER_BORDER) // 2,
                                    (BOARD_SIZE + OUTER_BORDER) // 2)
    popup_too_many_files.hide()
    popup_game_status.hide()
    return popup_too_many_files, popup_leaderboard_err, popup_game_status


def draw_gui_outlines():
    """Draw GUI outline rectangles on game window"""
    # tile area
    Rectangle(OUTER_BORDER, BOARD_SIZE, OUTER_BORDER, BOARD_SIZE, 5)
    # scoreboard
    Rectangle(OUTER_BORDER, BOARD_SIZE, BOARD_SIZE + INNER_BORDER,
              WINDOW_WIDTH - OUTER_BORDER, 5, "blue")
    # button area
    Rectangle(BOARD_SIZE + INNER_BORDER, WINDOW_HEIGHT - OUTER_BORDER,
              OUTER_BORDER, WINDOW_WIDTH - OUTER_BORDER, 5)


def calculate_tile_gap(tile_size):
    """Reduces default tile gap slightly for large tiles"""
    return min(DEFAULT_TILE_GAP, DEFAULT_TILE_GAP - min(tile_size - 100, 6))


def calculate_tile_border(tile_size):
    """Adjusts default tile placement slightly for large tiles"""
    return min(DEFAULT_TILE_BORDER, DEFAULT_TILE_BORDER - min(tile_size - 100, 3))


class Rectangle:
    """A rectangle object for use in gameboard GUI"""
    def __init__(self, top, bottom, left, right, line_width=1, color="black"):
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.color(color)

        self.height = top - bottom
        self.width = right - left

        self.turtle.penup()
        self.turtle.goto(left, top)
        self.turtle.pendown()
        self.turtle.width(line_width)

        for i in range(2):
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.right(90)


class SplashScreen:
    """A splash screen object for use when opening/closing the game"""
    def __init__(self, image, window_width=400, window_height=300):
        self.screen = turtle.Screen()
        self.screen.setup(window_width, window_height)
        self.screen.bgpic(image)
        self.screen.setworldcoordinates(- window_width / 2, -window_height / 2 - 10,
                                        window_width / 2, window_height / 2)
