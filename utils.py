import curses
import asyncio

from settings import (
    ROCKET_FILE_1_PATH,
    ROCKET_FILE_2_PATH,
    TRASH_LARGE_FILE,
    TRASH_SMALL_FILE,
)

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def get_canvas():
    canvas = curses.initscr()
    return canvas


def get_terminal_size():
    canvas = get_canvas()
    max_y, max_x = canvas.getmaxyx()
    return max_y, max_x


def convert_ms_to_iterations(ms):
    return ms * 10


def refresh_draw(canvas):
    canvas.border()
    canvas.refresh()


async def wait_time(secs):
    for _ in range(0, int(secs)):
        await asyncio.sleep(0)


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas.Erase text instead of drawing if negative=True is specified."""
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

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment.Returns pair (rows number, colums number)"""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def get_rocket_flame_1():
    with open(ROCKET_FILE_1_PATH) as f:
        return f.read()


def get_rocket_flame_2():
    with open(ROCKET_FILE_2_PATH) as f:
        return f.read()


def get_trash_large():
    with open(TRASH_LARGE_FILE) as trash_file:
        return trash_file.read()


def get_trash_small():
    with open(TRASH_SMALL_FILE) as trash_file:
        return trash_file.read()
