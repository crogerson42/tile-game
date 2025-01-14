"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

LoadMenu class contains a dictionary with all found valid puzzles.
It also contains a list of Buttons with thumbnails of all found valid puzzles.
These can be clicked on when the LoadMenu is shown on a screen, and which
thumbnail is selected is recorded.
"""
import turtle
from Button import Button
from file_functions import *


class LoadMenu:
    """
    LoadMenu creates a dictionary of all found valid puzzles, and a list of
    Buttons containing their thumbnails.  The menu and these buttons can be toggled
    to be shown or hidden. When shown, selection of a button can be recorded.
    """
    def __init__(self):
        """
        Creates a new LoadMenu class. Checks the game directory for valid puzzles,
        loads any found into its puzzle_directory dictionary, and creates a list
        of Buttons with the thumbnail images for each valid puzzle.
        """
        self.puzzle_selection = None
        self.menu_is_shown = False
        self.too_many_puzzles = False

        self.puzzle_directory, thumbnails = load_all_puzzles()
        self.thumbnail_turtles = self.create_thumbnails(thumbnails)

    def create_thumbnails(self, list_of_images):
        """
        Function -- create_thumbnails
            Takes a list of image files and returns a list of Button turtle objects
            displaying those images
        :param list_of_images: list of image file names to assign to Button turtle objects
        :return: list of newly created turtle objects with assigned images
        """
        turtle_list = []
        if len(list_of_images) > 9:
            self.too_many_puzzles = True
            number_to_display = 9
            log_error(f"More than 9 puzzle files found!")
        else:
            self.too_many_puzzles = False
            number_to_display = len(list_of_images)
        for i in range(number_to_display):
            t = Button(list_of_images[i], 120 + 150 * (i % 3),
                       120 + 150 * (i // 3), 150, 150)
            t.hide()
            turtle_list.append(t)
        return turtle_list

    def too_many(self):
        """
        Returns whether more puzzles were found than can be displayed as thumbnails
        :return: boolean: True if directory contains more than 9 puzzles, False otherwise
        """
        return self.too_many_puzzles

    def register_click(self, x, y):
        """
        Checks each displayed puzzle thumbnail Button to determine if it was clicked
        If a thumbnail ws clicked, the puzzle selection is set to the corresponding puzzle
        The "new thumbnail" animation plays, moving the button to the thumbnail position
        The menu is hidden and the screen is frozen to prepare for a new puzzle
        :param x: x-coordinate of screen click
        :param y: y-coordinate of screen click
        :return: None
        """
        for each in self.thumbnail_turtles:
            if each.register_click(x, y):
                each.state(False)
                # find the puzzle with the selected thumbnail; this is the selection
                thumbnail = each.get_image()
                for puzzle in self.puzzle_directory:
                    if self.puzzle_directory[puzzle]["thumbnail"] == thumbnail:
                        self.puzzle_selection = puzzle

                # hide the other options and move the button to the thumbnail position
                turtle.tracer(False)
                self.show_menu(False)  # hide menu
                each.show()  # re-show selected thumbnail
                turtle.tracer(True)
                each.use_as_new_thumbnail()

                # freeze the screen and move the button back to its menu location
                # the button will be replaced by a newly created thumbnail tile
                turtle.tracer(False)
                each.go_home()
                break  # do not continue iterating after finding the selected button

    def selection(self):
        """
        Returns the puzzle selected by the menu
        :return: string representing selected puzzle; used as key in self.puzzle_directory
        """
        return self.puzzle_selection

    def selected_puzzle_data(self):
        """
        Returns the puzzle data of the puzzle selected by the menu
        :return: dictionary representing selected puzzle
        """
        return self.puzzle_directory[self.selection()]

    def reset_selection(self):
        """Changes the selected puzzle back to None"""
        self.puzzle_selection = None

    def show_menu(self, boolean=None):
        """
        Get and set visibility of the LoadMenu object
        :param boolean: Optional; set menu visibility to True (shown) or False (hidden)
        :return: boolean value reflecting menu visibility: True if shown, False if hidden
        """
        if boolean is not None:
            self.menu_is_shown = boolean
            for each in self.thumbnail_turtles:
                if boolean:
                    each.show()
                else:
                    each.hide()
        return self.menu_is_shown
