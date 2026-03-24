from grid_io_1 import create_empty_grid

def apply_boundary_condition(grid, row, col):
    """
    Handles boundary conditions using a toroidal grid model.

    Args:
        grid (list[list[int]]): The current grid.
        row (int): The row index to check.
        col (int): The column index to check.

    Returns:
        tuple[int, int]: Adjusted (row, col) coordinates.
    """
    rows = len(grid)
    cols = len(grid[0])
    return row % rows, col % cols


def count_live_neighbors(grid, row, col):
    """
    Counts the number of live neighbors for a cell at given coordinates.

    Args:
        grid (list[list[int]]): The current state of the grid.
        row (int): The row index of the target cell.
        col (int): The column index of the target cell.

    Returns:
        int: The total count of living neighbors (0-8).
    """
    live_count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            
            neighbor_row = row + i
            neighbor_col = col + j
            
            valid_row, valid_col = apply_boundary_condition(grid, neighbor_row, neighbor_col)
            live_count += grid[valid_row][valid_col]
            
    return live_count


def next_generation(grid):
    """
    Computes and returns the next generation of the grid based on Conway's rules.

    Args:
        grid (list[list[int]]): The current grid state.

    Returns:
        list[list[int]]: A new grid representing the next generation.
    """
    rows = len(grid)
    cols = len(grid[0])
    new_grid = create_empty_grid(rows, cols)

    for r in range(rows):
        for c in range(cols):
            neighbors = count_live_neighbors(grid, r, c)
            is_alive = grid[r][c] == 1

            if is_alive:
                if neighbors == 2 or neighbors == 3:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1

    return new_grid