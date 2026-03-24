import random
import os

def create_empty_grid(rows, cols):
    """
    Creates an empty grid where all cells are dead.

    Args:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.

    Returns:
        list[list[int]]: A 2D list filled with zeros.
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]


def random_grid(rows, cols, prob=0.5):
    """
    Fills the grid with random values based on a survival probability.

    Args:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        prob (float): The probability (0.0 to 1.0) of a cell being alive.

    Returns:
        list[list[int]]: A 2D list with randomly distributed 0s and 1s.
    """
    grid = create_empty_grid(rows, cols)
    for row in range(rows):
        for col in range(cols):
            if random.random() < prob:
                grid[row][col] = 1
    return grid


def load_grid_from_file(filename):
    """
    Reads the grid configuration from a text file.

    Args:
        filename (str): The path to the file to be loaded.

    Returns:
        list[list[int]]: The grid loaded from the file or an empty grid if failed.
    """
    if not os.path.exists(filename):
        return create_empty_grid(10, 10)

    grid = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                row = [int(char) for char in clean_line if char in '01']
                grid.append(row)
    return grid


def save_grid_to_file(grid, filename):
    """
    Saves the current grid state to a text file.

    Args:
        grid (list[list[int]]): The 2D list to be saved.
        filename (str): The path to the destination file.

    Returns:
        None
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for row in grid:
            line = "".join(str(cell) for cell in row)
            f.write(line + "\n")


def set_cell(grid, row, col, value):
    """
    Sets the state of a specific cell in the grid.

    Args:
        grid (list[list[int]]): The 2D list to modify.
        row (int): Target row index.
        col (int): Target column index.
        value (int): New state (0 or 1).

    Returns:
        None
    """
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = value