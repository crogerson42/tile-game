"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Main function of the Tile Swap Game.  Displays a splash screen for several seconds on
startup, then prompts the player for their name and win condition. Creates a Gameboard
object to perform all following game functions.
"""
import turtle
from gui import SplashScreen
from Gameboard import Gameboard


def start_game(startup=True):
    """Prompts user for their name and win condition before opening a Gameboard object"""
    if startup:  # enable/disable startup choices
        player_name = turtle.textinput("Welcome!", "Your Name:")
        if player_name == "":
            player_name = "1UP"
        message = "Enter the number of moves you want: (5-200)"
        try:
            moves_to_win = int(turtle.numinput("Difficulty Selection", message,
                                               default=50, minval=5, maxval=200))
        except TypeError:
            moves_to_win = 50
    else:
        player_name = "1UP"
        moves_to_win = 200
    turtle.clearscreen()
    try:
        Gameboard(player_name, moves_to_win)
    except FileNotFoundError:
        pass  # default puzzle could not be loaded


def main():
    """Initiates the Tile Swap Game program; displays SplashScreen, then starts game"""
    SplashScreen("Resources/splash_screen.gif", 449, 373)
    turtle.ontimer(start_game, 500)
    turtle.mainloop()


if __name__ == '__main__':
    main()
