import pygame

"""
The windows used for the whole game
"""
window = None


def init_window() -> None:
    """
    Initializes the main window.
    """
    global window
    window = pg.display.set_mode((500, 500), pygame.RESIZABLE)
    pg.display.set_caption("Baba Is Clone")


init_window()
