import asyncio
import utils
from physics import update_speed
from settings import FIRE_SPEED
from sprites import fire
from utils import draw_frame, read_controls, get_frame_size
from global_vars import spaceship_frame, coroutines


def correct_row(max_available_row, current_row, row_frame):
    corrected_row = current_row
    if current_row >= max_available_row - row_frame:
        corrected_row = max_available_row - row_frame - 1
    elif current_row <= 0:
        corrected_row = 1
    return corrected_row


def correct_column(max_available_column, current_column, column_frame):
    corrected_column = current_column
    if current_column > max_available_column - column_frame:
        corrected_column = max_available_column - (column_frame + 1)
    elif current_column <= 1:
        corrected_column = 1
    return corrected_column


async def animate_spaceship(sprites):
    global spaceship_frame
    while True:
        for sprite in sprites:
            spaceship_frame = sprite
            await asyncio.sleep(0)


async def run_spaceship(canvas):
    global spaceship_frame
    global coroutines
    max_available_row, max_available_column = utils.get_terminal_size()
    row, column = max_available_row - 10, max_available_column / 2
    row_speed = column_speed = 0
    while True:
        row_frame, column_frame = get_frame_size(spaceship_frame)

        prev_sprite_row, prev_sprite_column = row, column
        prev_spaceship_frame = spaceship_frame
        canvas.nodelay(True)
        row_pos, column_pos, space = read_controls(canvas)

        draw_frame(canvas, prev_sprite_row, prev_sprite_column, spaceship_frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, row_pos, column_pos)
        row += row_pos + row_speed
        column += column_pos + column_speed
        if space:
            # for gun position in the center of the spaceship
            column_for_fire = column+2
            fire_animation = fire(canvas, row, column_for_fire, rows_speed=FIRE_SPEED)
            coroutines.append(fire_animation)
        row = correct_row(max_available_row, row, row_frame)
        column = correct_column(max_available_column, column, column_frame)

        draw_frame(canvas, row, column, spaceship_frame, negative=False)
        await asyncio.sleep(0)
        draw_frame(canvas, prev_sprite_row, prev_sprite_column, prev_spaceship_frame, negative=True)

