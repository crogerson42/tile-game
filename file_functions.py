"""
Christian Rogerson
CS 5002, Fall 2022
Tile Game Project

Contains functions for logging errors to a log file, finding valid puzzle files in the
game directory, loading a puzzle file, and loading all puzzle files.
"""
from os import listdir, path
from datetime import datetime
from math import sqrt

ERROR_FILE = "./Logs/error_log.err"
PUZZLE_DIR = "./Puzzles"


def log_error(error_message, print_to_console=False):
    """
    Append an error message (string) to a log file with a timestamp
    :param print_to_console: choose whether the error should also be printed to console
    :param error_message: string to be saved to error log file
    """
    with open(ERROR_FILE, mode='a') as out_file:
        error_output = f"{datetime.now()}: Error: {error_message}\n"
        out_file.write(error_output)
    if print_to_console:
        print(error_output)


def find_puzzles():
    """Return a list of all .puz files in the game directory"""
    puzzle_list = []
    for each in listdir(PUZZLE_DIR):
        if each[-4:] == ".puz":
            puzzle_list.append(each)
    return puzzle_list


def load_all_puzzles():
    """
    Load and check each .puz file in the game directory
    If it is valid, add it to a dictionary of valid puzzles,
    and add its thumbnail to a list of thumbnails
    :return: Dictionary of all valid puzzles, list of all thumbnail images
    """
    puzzle_list = find_puzzles()
    puzzle_dictionary = {}
    thumbnails_list = []
    for each in puzzle_list:
        puz = load_puzzle(each)
        if puz is not False:
            puzzle_dictionary[each] = puz
            thumbnails_list.append(puzzle_dictionary[each]['thumbnail'])
    return puzzle_dictionary, thumbnails_list


def load_puzzle(filename):
    """
    :param filename:
    :return: Dictionary containing 'name', 'number' (of tiles), 'size' (pixels),
    'tile_icons' (list of tile image files), 'thumbnail' (image filename)
    """
    try:
        metadata = {}
        with open(path.join(PUZZLE_DIR, filename), mode='r') as in_file:
            for line in in_file:
                key, value = line.strip("\n").split(": ")
                # process puzzle's number of tiles
                if key == 'number':
                    num_tiles = float(value)
                    if int(sqrt(num_tiles)) ** 2 != float(num_tiles):
                        raise SizeError  # puzzle is not square
                    metadata[key] = int(value)
                    metadata["tile_icons"] = [None] * int(value)
                # process puzzle's tile pixel size
                elif key == 'size':
                    metadata[key] = int(value)
                # process puzzle's name
                elif key == 'name':  # name should be assigned as-is (string)
                    metadata[key] = value
                # process puzzle's thumbnail image filename
                elif key == 'thumbnail':
                    if path.isfile(value):  # make sure thumbnail file exists
                        metadata[key] = value
                    else:  # thumbnail file could not be found
                        missing_file = value
                        raise ImageMissing
                # all other data is expected to be image numbers (ints)
                else:
                    if path.isfile(value):  # make sure image file exists
                        metadata["tile_icons"][int(key) - 1] = value  # add to icon list
                    else:  # tile image file could not be found
                        missing_file = value
                        raise ImageMissing
        # check that all required fields were loaded
        missing_data = []
        for each in ['name', 'number', 'size', 'thumbnail', 'tile_icons']:
            if each not in metadata:
                missing_data.append(each)
        for i in range(len(metadata['tile_icons'])):
            if metadata['tile_icons'][i] is None:
                missing_data.append(i + 1)
        if len(missing_data) != 0:
            raise DataError
        return metadata
    except FileNotFoundError:  # metadata file could not be found
        log_error(f"FileNotFoundError: File '{filename}' could not be found.")
        return False
    except TypeError:  # invalid filename input
        log_error(f"TypeError: Error reading '{filename}'.")
        return False
    except OSError:  # invalid filename input
        log_error(f"OSError: Error reading '{filename}'.")
        return False
    except KeyError:  # metadata file is missing 'number' (of tiles)
        log_error(f"KeyError: File '{filename}' is missing line 'number'.")
        return False
    except IndexError:  # metadata contained an image number exceeding 'number' of tiles
        log_error(f"IndexError: File '{filename}' contained extra or incorrect data. "
                  f"Error with line: {line}")
        return False
    except ValueError:  # metadata file contained a line beginning with an invalid key
        log_error(f"ValueError: File {filename} contained invalid data. "
                  f"Error with line: {line}")
        return False
    except DataError:  # metadata file missing one or more lines of data
        log_error(f"DataError: File '{filename}' was incomplete. "
                  f"Missing data: {', '.join(map(str, missing_data))}")
        return False
    except ImageMissing:  # metadata file referred to a nonexistent image file
        log_error(f"ImageMissing: File '{filename}' referenced a nonexistent file. "
                  f"Missing image: {missing_file}")
        return False
    except SizeError:  # puzzle size is not square
        log_error(f"SizeError: File {filename} contained an invalid puzzle size. "
                  f"Error with line: {line}")
        return False


class SizeError(Exception):
    """Puzzle size is not a square number"""
    pass


class DataError(Exception):
    """Metadata file was missing a required field"""
    pass


class ImageMissing(Exception):
    """Used to distinguish metadata file errors versus image file errors"""
    pass
