import asyncio
import curses

from utils.files_load_utils import get_gameover


def get_canvas():
    canvas = curses.initscr()
    return canvas


def get_frame_size(text):
    """Calculate size of multiline text fragment.Returns pair (rows number, colums number)"""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def get_terminal_size():
    canvas = get_canvas()
    max_y, max_x = canvas.getmaxyx()
    return max_y, max_x


def refresh_draw(canvas):
    canvas.border()
    canvas.refresh()


async def show_gameover(canvas):
    max_available_row, max_available_column = get_terminal_size()
    gameover_frame = get_gameover()
    rows, columns = get_frame_size(gameover_frame)
    center_row = (max_available_row / 2) - (rows / 2)
    center_column = (max_available_column / 2) - (columns / 2)
    while True:
        draw_frame(canvas,  center_row, center_column, gameover_frame)
        await asyncio.sleep(0)


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)
