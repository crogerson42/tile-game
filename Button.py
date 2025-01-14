"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Button Class defining turtles that can display images, and be clicked on.
Can keep track of whether they have been clicked on/inside.
Generally do not move, except for one simple animation.
"""
from ImageTurtle import ImageTurtle
from gui import THUMBNAIL_X, THUMBNAIL_Y, BUTTON_X_RIGHT, BUTTON_SPACING, BUTTON_Y


class Button(ImageTurtle):
    """Buttons are ImageTurtles that can be clicked on"""
    def __init__(self, image, x, y, width, height):
        """
        Creates an ImageTurtle object with additional Button features
        :param image: filename of image the turtle should represent graphically
        :param x: x-coordinate of turtle's home position
        :param y: y-coordinate of turtle's home position
        :param width: the visual width of the button (click region)
        :param height: the visual height of the button (click region)
        """
        super().__init__(image, x, y)
        self.button_state = False
        self.width = width
        self.height = height

    def register_click(self, x, y):
        """Check a button to see if it was clicked on"""
        x_click_inside = abs(x - self.get_x_home()) < self.get_width() / 2
        y_click_inside = abs(y - self.get_y_home()) < self.get_height() / 2
        if x_click_inside and y_click_inside:
            self.state(True)
        return self.state()

    def state(self, state=None):
        """
        Check or change a button's state
        :param state: If boolean, sets button's state to new boolean value
                      If None, state is unchanged
        :return: Boolean value of button's state
        """
        if state is not None:
            self.button_state = state
        return self.button_state

    def use_as_new_thumbnail(self):
        """Tells a button to move to the thumbnail position on the GUI"""
        self.turtle.speed(5)  # this is the only time a button needs visual speed
        self.turtle.goto(THUMBNAIL_X, THUMBNAIL_Y)
        self.turtle.speed(0)

    def get_width(self):
        """Returns button's width"""
        return self.width

    def get_height(self):
        """Returns button's height"""
        return self.height


def create_gui_buttons():
    """
    Create default Button objects
    :return: button_reset, button_load_other, button_load, button_quit
    """
    button_reset = Button("Resources/resetbutton.gif",
                          BUTTON_X_RIGHT - 3 * BUTTON_SPACING, BUTTON_Y, 80, 80)
    button_load_other = Button("Resources/loadotherbutton.gif",
                               BUTTON_X_RIGHT - 3 * BUTTON_SPACING, BUTTON_Y, 80, 80)
    button_load_other.hide()
    button_load = Button("Resources/loadbutton.gif",
                         BUTTON_X_RIGHT - 2 * BUTTON_SPACING, BUTTON_Y, 80, 80)
    button_quit = Button("Resources/quitbutton.gif",
                         BUTTON_X_RIGHT - 1 * BUTTON_SPACING, BUTTON_Y, 80, 55)
    return button_reset, button_load_other, button_load, button_quit
