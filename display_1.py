import pygame
from typing import List, Tuple, Optional


def init_display(rows: int, cols: int, cell_size: int = 20) -> Tuple[pygame.Surface, dict]:
    """
    Initializes the pygame window and display configuration.

    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        cell_size (int): Size of one cell in pixels.

    Returns:
        Tuple[pygame.Surface, dict]: The screen surface and configuration dictionary.
    """
    pygame.init()
    pygame.font.init()

    width = cols * cell_size
    height = rows * cell_size + 40
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of Life")

    font = pygame.font.SysFont("Arial", 20)
    config = {
        "rows": rows,
        "cols": cols,
        "cell_size": cell_size,
        "font": font,
        "colors": {
            "alive": (0, 200, 0),
            "dead": (30, 30, 30),
            "grid": (50, 50, 50),
            "bg": (10, 10, 10),
            "text": (255, 255, 255),
        }
    }
    return screen, config


def draw_grid(screen: pygame.Surface, grid: List[List[int]], config: dict) -> None:
    """
    Draws the grid based on the current state.

    Args:
        screen (pygame.Surface): The surface to draw on.
        grid (List[List[int]]): The current grid state.
        config (dict): The display configuration dictionary.

    Returns:
        None
    """
    rows = config["rows"]
    cols = config["cols"]
    cell_size = config["cell_size"]
    colors = config["colors"]

    screen.fill(colors["bg"])
    for row in range(rows):
        for col in range(cols):
            color = colors["alive"] if grid[row][col] else colors["dead"]
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, colors["grid"], rect, 1)


def draw_ui(screen: pygame.Surface, generation: int, speed: float, running: bool, config: dict) -> None:
    """
    Displays simulation information on the screen.

    Args:
        screen (pygame.Surface): The surface to draw on.
        generation (int): Current generation number.
        speed (float): Current simulation delay.
        running (bool): Whether the simulation is active.
        config (dict): The display configuration dictionary.

    Returns:
        None
    """
    font = config["font"]
    colors = config["colors"]
    y_offset = config["rows"] * config["cell_size"] + 5
    status = "Running" if running else "Paused"
    text = f"Gen: {generation} | Speed: {speed:.2f} | {status}"
    surface = font.render(text, True, colors["text"])
    screen.blit(surface, (10, y_offset))


def get_cell_from_mouse(pos: Tuple[int, int], config: dict) -> Optional[Tuple[int, int]]:
    """
    Converts mouse position to grid cell indices.

    Args:
        pos (Tuple[int, int]): Mouse position coordinates (x, y).
        config (dict): The display configuration dictionary.

    Returns:
        Optional[Tuple[int, int]]: Row and column indices or None if outside.
    """
    x, y = pos
    cell_size = config["cell_size"]
    row, col = y // cell_size, x // cell_size
    if 0 <= row < config["rows"] and 0 <= col < config["cols"]:
        return row, col
    return None