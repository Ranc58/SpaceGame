import asyncio
import utils
from utils import draw_frame, read_controls, get_frame_size


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


async def get_spaceship(canvas, sprites, speed=2):
    max_available_row, max_available_column = utils.get_terminal_size()
    row, column = max_available_row - 10, max_available_column / 2

    while True:
        row_frame, column_frame = get_frame_size(sprites[0])
        canvas.nodelay(True)
        row_pos, column_pos, space = read_controls(canvas)
        row += row_pos * speed
        column += column_pos * speed
        row = correct_row(max_available_row, row, row_frame)
        column = correct_column(max_available_column, column, column_frame)
        for sprite in sprites:
            draw_frame(canvas, row, column, sprite, negative=False)
            await asyncio.sleep(0)
            canvas.refresh()
            draw_frame(canvas, row, column, sprite, negative=True)
