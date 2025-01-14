"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

TileSet class keeps track of, and performs operations on, the Tiles of a sliding
tile game.  It is created from a dictionary of puzzle data.

Includes a "shuffle" function that performs a series of randomly chosen legal moves
(following certain rules) that GUARANTEES that a shuffled TileSet is solvable, because
in the worst case, a player could perfectly undo each move that was performed
while shuffling in reverse order.
"""
import turtle
from math import sqrt
from random import randint
from Tile import Tile
from ImageTurtle import ImageTurtle
from gui import THUMBNAIL_X, THUMBNAIL_Y, calculate_tile_border, calculate_tile_gap


class TileSet:
    """
    A set of n^2 Tile objects (plus a thumbnail object) reflecting a sliding puzzle
    The Tiles are represented graphically, and are also tracked logically in an
    n * n nested array: each Tile knows where it is, and the TileSet also knows
    where each tile is.

    Can shuffle itself, unscramble itself, check whether it has been clicked,
    perform legal moves, count its moves, and check whether it has been solved.
    """
    def __init__(self, puzzle_data: dict):
        """
        Create a new TileSet using a puzzle data dictionary to define
        the number of Tiles/puzzle width, image size of each Tile,
        and image files for use in each Tile (and the thumbnail ImageTurtle)
        """
        self.data = puzzle_data
        self.tile_size = (puzzle_data['size'])
        self.width = int(sqrt(puzzle_data['number']))
        self.moves = 0
        self.victory = False

        # create Tiles and thumbnail
        turtle.tracer(False)
        self.thumbnail = ImageTurtle(puzzle_data['thumbnail'], THUMBNAIL_X, THUMBNAIL_Y)
        self.tiles = []
        for row in range(self.width):
            new_row = []
            for column in range(self.width):
                new_row.append(Tile(puzzle_data['tile_icons'][column + row * self.width],
                                    column, row, self.tile_size))
            self.tiles.append(new_row)

        # Tell the blank tile that it is blank, hide it, and make it fast
        self.tiles[self.width - 1][self.width - 1].blank(True)
        self.tiles[self.width - 1][self.width - 1].hide()
        self.tiles[self.width - 1][self.width - 1].change_speed(0)
        self.the_blank = self.blank_location(self.width - 1, self.width - 1)

        self.is_shuffling = False

    def move_count(self):
        """Returns the count of how many moves have been performed"""
        return self.moves

    def set_speed(self, speed):
        """Sets the speed of every Tile in the TileSet"""
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                self.tiles[i][j].change_speed(speed)

    def blank_location(self, column=None, row=None):
        """
        Instructs the TileSet to remember a new blank location, if one is provided.
        Returns the currently or newly logged blank location.
        :param column: If provided with row, record column as the location of the blank
        :param row: If provided with column, record row as the location of the blank
        :return: The current location of the blank tile (column, row)
        """
        if column in range(self.width) and row in range(self.width):
            self.the_blank = column, row
        return self.the_blank

    def shuffle(self, swaps=100, speed=0, trace=True):
        """
        Function -- shuffle
            Shuffles the tiles by performing legal swaps. Randomly chooses to perform
            a horizontal or vertical swap. If the blank tile is at the edge of the
            game board (max or min), it is moved towards the center.

            Otherwise, if the selected movement axis (horizontal or vertical) is the
            same as the previous move, the blank is moved so that the previous move
            is NOT undone.

            Otherwise, if the previous move was in a different axis and the blank
            is not at the gameboard edge, the blank is randomly swapped in one of
            the directions along the chosen axis.

            This ensures that successive randomly selected moves generally
            increase, rather than decrease, the entropy of the gameboard.

            Additionally, since all shuffling is performed using legal moves,
            it is GUARANTEED that the puzzle is still solvable, as in the worst
            case the moves used to shuffle could be undone in reverse order.
        :param swaps: the number of swaps to perform (default = 100)
            A larger number of swaps results in a more randomized tile layout
        :param speed: the speed of swaps to perform (default = 0: instant)
            0 = instant; 9 = fast; 1 = very slow
        :param trace: boolean reflecting screen updates to show shuffling steps
            True (default): shuffle animation plays
            False: shuffle is completed almost immediately
        """
        original_trace_state = turtle.tracer()
        turtle.tracer(trace)
        self.set_speed(speed)
        self.is_shuffling = True
        last_move = 5

        for swap in range(swaps):
            # check current location of blank tile
            column, row = self.blank_location()
            # 50% chance of vertical swap
            if randint(0, 1) == 1:
                # tile in min row; can't move down
                if row == 0:
                    modifier = 1
                    last_move = 2
                # tile in max row; can't move up
                elif row + 1 == self.width:
                    modifier = -1
                    last_move = 4
                # don't undo the last move if it was also horizontal
                elif last_move < 5:
                    modifier = 3 - last_move
                # randomly select +1 or -1
                else:
                    modifier = 2 * randint(0, 1) - 1
                    last_move = 3 + modifier
                self.swap_tiles(column, row + modifier, column, row)
                self.blank_location(column, row + modifier)
            # 50% chance of horizontal swap
            else:
                # tile in min column; can't move left
                if column == 0:
                    modifier = 1
                    last_move = 6
                # tile in max column; can't move right
                elif column + 1 == self.width:
                    modifier = -1
                    last_move = 8
                # don't undo the last move if it was also vertical
                elif last_move > 5:
                    modifier = 7 - last_move
                # randomly select +1 or -1
                else:
                    modifier = 2 * randint(0, 1) - 1
                    last_move = 7 + modifier
                self.swap_tiles(column + modifier, row, column, row)
                self.blank_location(column + modifier, row)
        self.set_speed(3)
        self.is_shuffling = False
        turtle.tracer(original_trace_state)

    def unscramble(self):
        """
        All tiles are moved back to their home locations. The tiles array
        is replaced with a new array that is properly ordered in order
        of home position, as when the TileSet was first created.
        """
        unscrambled_tiles = []
        for row in range(self.width):
            new_row = []
            for column in range(self.width):
                new_row.append([None])
            unscrambled_tiles.append(new_row)
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                tile = self.tiles[i][j]
                # tile moves to correct physical location
                x_home, y_home = tile.go_home()
                unscrambled_tiles[y_home][x_home] = tile
        # tiles re-ordered in array
        self.tiles = unscrambled_tiles
        self.the_blank = self.blank_location(self.width - 1, self.width - 1)

    def register_click(self, x, y):
        """
        Checks whether the coordinates of a screen click are on one of its tiles.
        If so, checks whether the clicked tile is next to (but not itself) the
        blank tile. If so, a legal swap is possible, and is performed. If a swap is
        performed, the puzzle then checks itself to determine if it is solved.
        :param x: x-coordinate of click on screen
        :param y: y-coordinate of click on screen
        :return: False if click is outside TileSet; True if click is inside TileSet
        """
        column = int((x - calculate_tile_border(self.tile_size) + self.tile_size // 2) /
                     (self.tile_size + calculate_tile_gap(self.tile_size)))
        row = int((y - calculate_tile_border(self.tile_size) +
                   self.tile_size // 2) /
                  (self.tile_size + calculate_tile_gap(self.tile_size)))
        if row not in range(0, self.width) or column not in range(0, self.width):
            return False

        neighbor_is_blank = self.check_neighbors(column, row)
        if neighbor_is_blank is not False:
            self.swap_tiles(column, row, neighbor_is_blank[0], neighbor_is_blank[1])
            self.blank_location(column, row)
            if self.is_solved():
                self.victory = True
        return True

    def check_neighbors(self, column, row):
        """
        Determines whether the column OR row difference (but not both) between
        a selected tile and the blank tile is exactly 1. If so, return the
        coordinates of the blank tile. Otherwise, return False.
        :param column: column reference of selected tile
        :param row: row reference of selected tile
        :return: (column, row) of blank tile (if adjacent); False otherwise
        """
        col_dif = abs(column - self.blank_location()[0])
        row_dif = abs(row - self.blank_location()[1])
        if (col_dif + row_dif) == 1:
            return self.blank_location()
        else:
            return False

    def swap_tiles(self, column_1, row_1, column2, row_2):
        """
        Swaps two tiles physically on the GUI as well as logically in the tiles array
        :param column_1: column reference (x) of first tile
        :param row_1: row reference (y) of first tile
        :param column2: column reference (x) of second tile
        :param row_2: row reference (y) of second tile
        """
        a, b, c, d = row_1, column_1, row_2, column2
        # swap tiles physically - tiles should know where they are
        self.tiles[row_1][column_1].move(d, c)
        self.tiles[row_2][column2].move(b, a)
        # swap tiles in array - tileset should know where tiles are
        self.tiles[a][b], self.tiles[c][d] = self.tiles[c][d], self.tiles[a][b]

        if not self.is_shuffling:
            self.moves += 1

    def is_solved(self):
        """
        Checks every tile to determine if each is 'home'. If all tiles are home,
        return True; if any tile is not home, return false.
        """
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if not self.tiles[i][j].is_home():
                    return False
        return True

    def victory_achieved(self):
        """Returns True if the puzzle has been solved; returns False otherwise"""
        return self.victory

    def reset(self):
        """Makes each tile disappear in preparation for deletion/replacement"""
        turtle.tracer(False)
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                self.tiles[row][column].disappear()
        self.thumbnail.disappear()
        turtle.tracer(True)
