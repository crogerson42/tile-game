# Tile Game Project

**Christian Rogerson** 
**Fall 2022**

---- Overview: ----

This project implements a sliding tile puzzle game using Python and the Python turtle library in an object-oriented approach.  My shuffling algorithm guarantees solvable puzzles by only shuffling tiles using legal moves that could be reversed to solve the puzzle.  I also redesigned the load menu to provide an easy and error-resistant graphical user interface by representing all valid loadable puzzles as clickable thumbnail images.

---- Design: ----

Much of my game is based off "ImageTurtle" objects which are objects containing turtles displaying defined image files.  "Tiles" and "Buttons" are ImageTurtles that can move and be clicked on, respectively.

The primary driving function of my program is the overarching Gameboard class's register_click: this passes the click's (x, y) coordinates to each relevant graphical object in turn.  This protocol allows the Gameboard to handle all central decision-making, while allowing each object to react appropriately and dividing up their click reactions.

---- Source Files: ----

Python Files:
> puzzle_game.py - location of "main()"; creates Gameboard object
> Gameboard.py - contains all other objects and data; handles clicks and decision-making; drives program

> LoadMenu.py - contains all loaded puzzle data, and can represent puzzle choices graphically
> Leaderboard.py - reads, graphically represents, and saves score information
> TileSet.py - contains all game tiles, knows where they are, and performs actions on them

> Tile.py - an ImageTurtle that can move around the game grid
> Button.py - an ImageTurtle that can register being clicked on
> ImageTurtle.py - a basic turtle displaying an image

> TextTurtle.py - a basic turtle that can write
> gui.py - contains functions and classes to create GUI elements; also contains all GUI-defining constants
> file_functions.py - functions to log errors, load puzzles, and search directory for valid puzzles

Graphics Reskins:
> "file_warning_9.gif" - reskin of "file_warning.gif" to reflect that a maximum of 9 puzzle thumbnails can be shown in the 3x3 grid of my load menu GUI
> "loadotherbutton.gif" - reskin of "loadbutton.gif" to allow access to a secondary, text-based load function instead of the default GUI

---- Instructions for use ----

> GUI Reskin - Puzzle Loading:
I wanted to make the game as user-friendly and enjoyable as possible.  To start, I added a graphical loading menu when loading a puzzle.  This requires fewer user actions as well as avoiding unnecessary errors.  Text entry is still available, but by default, I provided thumbnails of valid puzzles that the program finds in its directory and pre-validates.  The user is able to click on these to select a puzzle, which provides a small but satisfying animation as the selected button becomes the new "clue" thumbnail image.

> Shuffling Algorithm:
While I did not end up producing the verification code or PyUnit testing required to receive a bonus, I tried for bonus points by developing a shuffling algorithm that produces a sufficiently random puzzle using only legal tile swaps, which 100% guarantees that all puzzles produced by my game are solvable.

The shuffle algorithm selects each move to increase the total entropy of the tile arrangement: the algorithm avoids randomly selecting moves that undo the previous move so that each move makes the puzzle more challenging and satisfying to solve.  The shuffle animation itself is also satisfying (hopefully further adding to user experience).  

> Other UI/Feedback to User:
Sliding animations continue into gameplay, where clicking on each tile shows it sliding into the adjacent blank space.  The sliding animation, shuffling animation, and load thumbnail animation - the three "A"'s - make this, technically speaking, a triple-A game.

Also note that when you have less than 10 moves remaining, the move counter will change to red to increase the player's tension, and draw attention to it.  Be to initiate a game with a small number of moves if you want to witness this.

---- Citations/References/Shoutouts ----

Thanks to Professor Keith and the TAs - especially Jarred and Chandler - for a great semester!  See you in the spring!
