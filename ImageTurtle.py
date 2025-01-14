"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

ImageTurtle Class defining turtles that can display images.
Cannot move or react, but have a defined position and can hide/show themselves.
"""
import turtle


class ImageTurtle:
    """
    A basic class of turtle with a defined image,
    for representing graphical objects
    """
    def __init__(self, image, x, y, speed=0):
        """
        Creates an ImageTurtle object
        :param image: filename of image the turtle should represent graphically
        :param x: x-coordinate of turtle's home position
        :param y: y-coordinate of turtle's home position
        """
        self.turtle = create_turtle(speed)
        self.speed = speed

        turtle.addshape(image)
        self.turtle.shape(image)

        self.image = image
        self.x_home = x
        self.y_home = y
        self.go_home()

    def hide(self):
        """Hides the ImageTurtle"""
        self.turtle.hideturtle()

    def show(self):
        """Shows the ImageTurtle"""
        self.turtle.showturtle()

    def get_x_home(self) -> int:
        """Returns ImageTurtle's home x position"""
        return self.x_home

    def get_y_home(self) -> int:
        """Returns ImageTurtle's home y position"""
        return self.y_home

    def go_home(self):
        """
        Tells the ImageTurtle to return to its home position
        :return: x coordinate of home position, y coordinate of home position
        """
        self.turtle.goto(self.get_x_home(), self.get_y_home())
        return self.get_x_home(), self.get_y_home()

    def get_image(self):
        """Returns the (filename of the) ImageTurtle's image"""
        return self.image

    def change_image(self, image):
        """
        Setter for the object's image
        Also replaces the object's existing turtle with a new one
        on the top layer of the GUI
        """
        tracer_state = turtle.tracer()  # log current tracer state
        turtle.tracer(False)
        self.disappear()  # hide old turtle
        self.turtle = create_turtle(self.speed)  # create new turtle on top layer

        # set new turtle's image to desired image
        turtle.addshape(image)
        self.turtle.shape(image)
        self.image = image

        # move new turtle to old turtle's location
        self.go_home()
        turtle.tracer(tracer_state)  # resets tracer state

    def disappear(self):
        """Hides the tile's turtle object in preparation for replacement"""
        self.turtle.reset()
        self.turtle.hideturtle()


def create_turtle(speed=0):
    """Creates a turtle with default values"""
    new_turtle = turtle.Turtle()
    new_turtle.speed(speed)
    new_turtle.penup()
    return new_turtle
