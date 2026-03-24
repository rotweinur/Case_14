import sys
import pygame
from grid_io_1 import (
    create_empty_grid, random_grid, load_grid_from_file,
    save_grid_to_file, set_cell
)
from logic_1 import next_generation
from display_1 import init_display, draw_grid, draw_ui, get_cell_from_mouse


def handle_events(grid, initial_grid, running, speed, generation, config):
    """
    Processes Pygame events such as keyboard and mouse inputs.

    Args:
        grid (list[list[int]]): Current state of the grid.
        initial_grid (list[list[int]]): Initial grid state for resetting.
        running (bool): Simulation activity flag.
        speed (float): Simulation delay in seconds.
        generation (int): Current generation count.
        config (dict): Display configuration dictionary.

    Returns:
        tuple: Updated values (grid, initial_grid, running, speed, generation, app_running).
    """
    app_running = True
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                app_running = False
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        app_running = False
                    case pygame.K_SPACE:
                        running = not running
                    case pygame.K_s | pygame.K_RIGHT:
                        grid = next_generation(grid)
                        generation += 1
                    case pygame.K_r:
                        grid = [row[:] for row in initial_grid]
                        generation, running = 0, False
                    case pygame.K_c:
                        grid = create_empty_grid(len(grid), len(grid[0]))
                        initial_grid = [row[:] for row in grid]
                        generation, running = 0, False
                    case pygame.K_l:
                        try:
                            grid = load_grid_from_file("config.txt")
                            initial_grid = [row[:] for row in grid]
                            generation, running = 0, False
                        except Exception:
                            pass
                    case pygame.K_f:
                        save_grid_to_file(grid, "config.txt")
                    case pygame.K_PLUS | pygame.K_KP_PLUS | pygame.K_EQUALS:
                        speed = max(0.02, speed - 0.05)
                    case pygame.K_MINUS | pygame.K_KP_MINUS:
                        speed = min(2.0, speed + 0.05)
                    case pygame.K_t:
                        config["lang"] = "en" if config["lang"] == "ru" else "ru"
                        pygame.display.set_caption(config["translations"][config["lang"]]["title"])
            case pygame.MOUSEBUTTONDOWN | pygame.MOUSEMOTION:
                btns = pygame.mouse.get_pressed()
                if btns[0] or btns[2]:
                    coords = get_cell_from_mouse(pygame.mouse.get_pos(), config)
                    if coords:
                        set_cell(grid, coords[0], coords[1], 1 if btns[0] else 0)
                        
    return grid, initial_grid, running, speed, generation, app_running


def main():
    """
    The main execution function that initializes the game and runs the loop.

    Returns:
        None
    """
    rows, cols, cell_size = 40, 40, 20
    speed, running, generation = 0.1, False, 0
    screen, config = init_display(rows, cols, cell_size, lang="ru")
    clock = pygame.time.Clock()
    grid = random_grid(rows, cols, prob=0.3)
    initial_grid = [row[:] for row in grid]
    last_update = pygame.time.get_ticks()
    app_running = True

    while app_running:
        grid, initial_grid, running, speed, generation, app_running = handle_events(
            grid, initial_grid, running, speed, generation, config
        )
        now = pygame.time.get_ticks()
        if running and (now - last_update) >= int(speed * 1000):
            grid = next_generation(grid)
            generation += 1
            last_update = now
            
        draw_grid(screen, grid, config)
        draw_ui(screen, generation, speed, running, config)
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()