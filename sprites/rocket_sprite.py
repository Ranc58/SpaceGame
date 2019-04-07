import asyncio
import utils
from utils import draw_frame, read_controls, get_frame_size


def correct_spaceship_position(
        row_max, row, row_frame, column_max, column, column_frame
):
    corrected_row, corrected_column = row, column
    if row_max - row <= row_frame:
        corrected_row = row_max - row_frame - 1
    elif row <= 0:
        corrected_row = 1

    if column > column_max - (column_frame + 1):
        corrected_column = column_max - (column_frame + 1)
    elif column <= 1:
        corrected_column = 1
    return corrected_row, corrected_column


async def space_ship(canvas, sprites, speed=2):
    row_max, column_max = utils.get_terminal_size()
    ship_position = []
    if not ship_position:
        ship_position.append(row_max - 10)
        ship_position.append(column_max / 2)

    while True:
        row_frame, column_frame = get_frame_size(sprites[0])

        canvas.nodelay(True)
        row_pos, column_pos, space = read_controls(canvas)
        row = ship_position[0] + row_pos * speed
        column = ship_position[1] + column_pos * speed

        row, column = correct_spaceship_position(
            row_max, row, row_frame, column_max, column, column_frame
        )

        for sprite in sprites:
            draw_frame(canvas, row, column, sprite, negative=False)
            await asyncio.sleep(0)
            canvas.refresh()
            draw_frame(canvas, row, column, sprite, negative=True)

        ship_position[0] = row
        ship_position[1] = column
