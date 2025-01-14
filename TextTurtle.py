"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

TextTurtle Class defining turtles that can write text at their location.
"""
import turtle
from ImageTurtle import create_turtle


class TextTurtle:
    """
    A basic class of turtle with a defined location that can be
    instructed to write things at its location
    """
    def __init__(self, x, y, color='blue'):
        """
        Creates a TextTurtle object
        :param color: color name (string) to use for writing
        :param x: x-coordinate of turtle's home position
        :param y: y-coordinate of turtle's home position
        """
        self.turtle = create_turtle()
        self.turtle.hideturtle()
        self.turtle.goto(x, y)

        self.default_color = color
        self.turtle.color(color)

    def change_color(self, color):
        """Set current turtle color"""
        self.turtle.color(color)

    def write(self, text, size=20, style='normal'):
        """
        Tells the turtle to write text at its location
        :param text: String for the turtle to write
        :param size: Font size (default 20)
        :param style: Font style ('normal', 'bold', etc.)
        """
        self.turtle.write(arg=text, align='left', font=('Arial', size, style))

    def write_score(self, numerator, denominator):
        """
        A specialized write function for writing the move count
        :param numerator: string representing numerator of fraction (moves used)
        :param denominator: string representing denominator of fraction (max moves)
        """
        tracer_status = turtle.tracer()
        turtle.tracer(False)
        self.clear()
        self.write(f"Moves: {numerator} / {denominator}", style='bold')
        turtle.tracer(tracer_status)

    def clear(self):
        """Clears text previously written by the turtle"""
        self.turtle.clear()

    def reset_color(self):
        """Restores the turtle's default color"""
        self.turtle.color(self.default_color)
