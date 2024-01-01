import pygame as py
import pygame.gfxdraw as pgfx

def __history_dimensions(list: list, letter_size: int) -> tuple:
    """Takes the history list and sizes of letters and returns the needed size for the history window."""
    width = 0
    for score in list:
        if len(score) > width:
            width = len(score)
    height = letter_size + letter_size // 2
    return width * (round(letter_size / 2.4)), height

def matchhistory(list: list) -> None:
    """Displays the history in a new window."""
    py.init()
    letter_size = 30
    width, height = __history_dimensions(list, letter_size)
    window = py.display.set_mode((width, height * len(list)))
    py.display.set_caption("Previous games")
    fgcolor = py.Color('LightYellow')
    bgcolors = [py.Color('#990099'), py.Color('#009933')]
    font = py.font.SysFont('Arial', letter_size)
    for ind in range(len(list)):
        pgfx.box(window, py.Rect(0, ind * height, width, height - letter_size // 4), bgcolors[ind % 2])
        text = font.render(list[ind], True, fgcolor)
        window.blit(text, (4, ind * height))
    py.display.update()
    quit = False
    while not quit:
        event = py.event.wait()
        if event.type == py.QUIT:
            quit = True
    py.quit()

def draw_info(window: object, title: str, list: list, starting: int) -> None:
    """Draws a string list's elements onto the given window based on height."""
    title_font = py.font.SysFont('Arial Bold', 30)
    title_fgcolor = py.Color('SkyBlue')
    text_font = py.font.SysFont('Arial', 16)
    text_fgcolor = py.Color('Yellow')
    text = title_font.render(title, True, title_fgcolor)
    window.blit(text, (40, starting))
    for ind in range(len(list)):
        text = text_font.render(list[ind], True, text_fgcolor)
        window.blit(text, (4, ind * 18 + 30 + starting))

def info() -> None:
    """Displays the control information in a new window."""
    py.init()
    window = py.display.set_mode((420, 280))
    py.display.set_caption("Controls")
    window.fill(py.Color("DimGray"))
    mousecontrols = ["Unit/terrain selection: left-click on a tile."
            , "  - Left-click on the tile again to unselect the unit."
            , "  - For factory: left-click again to list units."
            , "      - Left-click on a purchasable unit to have it spawn."
            , "Unit movement: left-click on a valid adjacent tile."
            , "Unit attack: right-click on a unit in range."
            , "Unit capture: right-click on the tile the unit is on."
            , "End turn: left-click on the \"End Turn\" button."
            , "Exit: left-click on the \"Exit\" button."]
    keyboardcontrols = ["Movement: W/^ - Up, A/< - Left, S/ˇ - Down, D/> - Right"
            , "Capture: Space, End turn: Enter, Exit: Escape"]
    draw_info(window, "Mouse", mousecontrols, 4)
    draw_info(window, "Keyboard", keyboardcontrols, 210)
    py.display.update()
    quit = False
    while not quit:
        event = py.event.wait()
        if event.type == py.QUIT:
            quit = True
    py.quit()