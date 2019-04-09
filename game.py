import _curses
import asyncio
import time
import random
import curses

import utils
from sprites import blink, fire
from sprites.trash_sprite import fly_garbage
from sprites.rocket_sprite import get_spaceship
from settings import SPACESHIP_SPEED, STARS_COUNT, FIRE_SPEED, TIC_TIMEOUT

coroutines = []

def get_stars(canvas, stars_count=80):
    stars = []
    max_y, max_x = utils.get_terminal_size()
    for _ in range(0, stars_count):
        symbol = random.choice('+*.:')
        y_coord = random.randint(1, max_y - 1)
        x_coord = random.randint(1, max_x - 1)
        waiting_time = random.randint(0, 20)
        star = blink(canvas, y_coord, x_coord, symbol, waiting_time)
        stars.append(star)
    return stars


def get_fire(canvas):
    max_y, max_x = utils.get_terminal_size()
    return fire(canvas, max_y - 11, round(max_x / 2) + 2, rows_speed=FIRE_SPEED)


def get_trash(canvas):
    sizes_map = {
        'large': utils.get_trash_large,
        'small': utils.get_trash_small,
    }
    _, max_x = utils.get_terminal_size()

    columns = max_x - 1
    trash_size = random.choice(['large', 'small'])
    trash_frame = sizes_map[trash_size]()
    column_for_trash = random.randint(1, columns)
    await_time = random.randint(0, 20)
    trash = fly_garbage(canvas, column_for_trash, trash_frame, await_time)

    return trash


async def fill_orbit_with_garbage(canvas):
    global coroutines
    start_len = len(coroutines)
    while True:
        if len(coroutines) < start_len:
            coroutines.append(get_trash(canvas))
        await asyncio.sleep(0)


def main(canvas, rocket_frame_1, rocket_frame_2):
    curses.curs_set(False)
    global coroutines

    fire_animation = get_fire(canvas)
    coroutines.append(fire_animation)

    stars = get_stars(canvas, STARS_COUNT)
    coroutines += stars

    spaceship = get_spaceship(
        canvas, [rocket_frame_1, rocket_frame_2], SPACESHIP_SPEED
    )
    coroutines.append(spaceship)

    for _ in range(0, 5):
        garbage = get_trash(canvas)
        coroutines.append(garbage)
    coroutines.append(fill_orbit_with_garbage(canvas))
    while True:
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)
            except RuntimeError:
                coroutines.remove(coro)
            except _curses.error:
                continue
            if len(coroutines) == 0:
                break
            utils.refresh_draw(canvas)
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    try:
        rocket_frame_1 = utils.get_rocket_flame_1()
        rocket_frame_2 = utils.get_rocket_flame_2()
    except FileNotFoundError as e:
        print(f'Not found "{e.filename}"')
        exit()
    curses.update_lines_cols()
    curses.wrapper(main, rocket_frame_1, rocket_frame_2)
