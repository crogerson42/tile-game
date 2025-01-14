"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Tile Class defining turtles that can display images, and move around on a game grid.
Can move, go home, know where they are, and know if they are home.
"""
from ImageTurtle import ImageTurtle
from gui import calculate_tile_border, calculate_tile_gap


class Tile(ImageTurtle):
    """Tiles are ImageTurtles that can move around on a game grid"""
    def __init__(self, image, x, y, tile_size):
        """
        Creates a Tile object with a defined image, position, and size
        :param image: string of filename from which to load image
        :param x: x-position of tile - initially used for both current and home
        :param y: y-position of tile - initially used for both current and home
        :param tile_size: size of the tile; used for proper scaling
        """
        self.x_location = x
        self.y_location = y
        self.width_of_tile = tile_size
        super().__init__(image, x, y, speed=3)
        self.is_blank = False

    def blank(self, blank=None):
        """
        Check or change whether a tile is blank
        :param blank: If boolean, sets tile's state to new boolean value
                      If None, state is unchanged
        :return: Boolean value of whether a tile is blank
        """
        if type(blank) == bool:
            self.is_blank = blank
        return self.is_blank

    def change_speed(self, speed):
        """Set's the Tile's turtle speed"""
        self.turtle.speed(speed)

    def go_home(self) -> tuple:
        """
        Overrides ImageTurtle's go_home() method to use game grid coordinates
        :return: x coordinate of home position, y coordinate of home position
        """
        self.move(self.get_x_home(), self.get_y_home())
        return self.get_x_home(), self.get_y_home()

    def move(self, x, y):
        """
        Setter for the object's x-y coordinates
        Also moves the turtle to the corresponding graphical location
        :param x: new x location
        :param y: new y location
        """
        self.x_location = x
        self.y_location = y
        # move tile to location on the defined game grid
        x_screen, y_screen = game_grid_to_screen_coord(x, y, self.tile_size())
        self.turtle.goto(x_screen, y_screen)

    def tile_size(self):
        """Returns Tile's size (for GUI scaling)"""
        return self.width_of_tile

    def current_x(self):
        """Returns Tile's current x position"""
        return self.x_location

    def current_y(self):
        """Returns Tile's current y position"""
        return self.y_location

    def is_home(self):
        """
        Checks whether a tile's current position is also its home position
        :return: boolean (True if yes, False if no)
        """
        x_is_home = self.current_x() == self.get_x_home()
        y_is_home = self.y_location == self.get_y_home()
        if x_is_home and y_is_home:
            return True
        return False


def game_grid_to_screen_coord(x_grid, y_grid, scale):
    """
    Convert game grid x-y coordinates to screen x-y coordinates
    Used to convert game logic/tile placement to screen drawings
    :param x_grid: x-coordinate on game grid (i.e. 0-3)
    :param y_grid: y-coordinate on game grid (i.e. 0-3)
    :param scale: width of each tile to be used for scaling
    :return: screen x-coordinate, screen y-coordinate
    """
    x_screen = x_grid * (scale + calculate_tile_gap(scale)) + calculate_tile_border(scale)
    y_screen = y_grid * (scale + calculate_tile_gap(scale)) + calculate_tile_border(scale)
    return x_screen, y_screen
