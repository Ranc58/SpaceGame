import curses
import asyncio


from settings import (
    ROCKET_FILE_1_PATH,
    ROCKET_FILE_2_PATH,
    TRASH_LARGE_FILE,
    TRASH_SMALL_FILE,
    DUCK_FILE,
    LAMP_FILE,
    TRASH_XL_FILE,
    HUBBLE_FILE,
    GAMEOVER_FILE,
)

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


def get_canvas():
    canvas = curses.initscr()
    return canvas


def get_terminal_size():
    canvas = get_canvas()
    max_y, max_x = canvas.getmaxyx()
    return max_y, max_x


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


def get_message(year):
    phrase = PHRASES.get(year)
    message = year
    if phrase:
        message = f'{year}: {phrase}'
    return message


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


def get_trash_xl():
    with open(TRASH_XL_FILE) as trash_file:
        return trash_file.read()


def get_duck():
    with open(DUCK_FILE) as duck:
        return duck.read()


def get_hubble():
    with open(HUBBLE_FILE) as hubble:
        return hubble.read()


def get_lamp():
    with open(LAMP_FILE) as lamp:
        return lamp.read()


def get_gameover():
    with open(GAMEOVER_FILE) as gameover:
        return gameover.read()


async def show_gameover(canvas):
    max_available_row, max_available_column = get_terminal_size()
    gameover_frame = get_gameover()
    rows, columns = get_frame_size(gameover_frame)
    center_row = (max_available_row / 2) - (rows / 2)
    center_column = (max_available_column / 2) - (columns / 2)
    while True:
        draw_frame(canvas,  center_row, center_column, gameover_frame)
        await asyncio.sleep(0)


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
