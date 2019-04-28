import asyncio

from obstacles_code import Obstacle, show_obstacles
from sprites.explosion_sprite import explode
from utils import draw_frame, wait_time
from global_vars import obstacles, coroutines, obstacles_in_last_collisions
import utils


async def fly_garbage(canvas, column, garbage_frame, await_time=10, speed=0.8):
    global obstacles
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)
    row = 0
    rows, columns = utils.get_frame_size(garbage_frame)
    await wait_time(await_time)
    obstacle = Obstacle(row, column, rows, columns)
    obstacles.append(obstacle)
    while row < rows_number:

        draw_frame(canvas, row, column, garbage_frame)
        obstacle.row = row

        await asyncio.sleep(0)

        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row += speed
        if obstacle in obstacles_in_last_collisions:
            explode_row = row + (rows/2)
            explode_column = column + (columns/2)
            await explode(canvas, explode_row, explode_column)
            obstacles.remove(obstacle)
            return
    obstacles.remove(obstacle)


