import _curses
import asyncio
import time
import random
import curses

import utils
from obstacles_code import show_obstacles
from sprites import blink, fire
from sprites.trash_sprite import fly_garbage
from sprites.rocket_sprite import animate_spaceship, run_spaceship
from settings import STARS_COUNT, FIRE_SPEED, TIC_TIMEOUT, TRASH_START_COUNT
from global_vars import coroutines
from global_vars import obstacles


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
        'xl': utils.get_trash_xl,
        'hubble': utils.get_hubble,
        'lamp': utils.get_lamp,
        'duck': utils.get_duck,
    }
    _, max_x = utils.get_terminal_size()
    columns = max_x - 1
    list_sizes_keys = list(sizes_map.keys())
    trash_size = random.choice(list_sizes_keys)
    trash_frame = sizes_map[trash_size]()
    column_for_trash = random.randint(1, columns)
    await_time = random.randint(0, 50)
    trash = fly_garbage(canvas, column_for_trash, trash_frame, await_time)

    return trash


async def fill_orbit_with_garbage(canvas):
    global coroutines
    global obstacles
    while True:
        if len(obstacles) < TRASH_START_COUNT:
            coroutines.append(get_trash(canvas))
        await asyncio.sleep(0)


def main(canvas, rocket_frame_1, rocket_frame_2):
    curses.curs_set(False)
    global coroutines

    spaceship_frame = animate_spaceship([rocket_frame_1, rocket_frame_2])
    coroutines.append(spaceship_frame)

    spaceship = run_spaceship(canvas)
    coroutines.append(spaceship)

    fire_animation = get_fire(canvas)
    coroutines.append(fire_animation)

    stars = get_stars(canvas, STARS_COUNT)
    coroutines += stars

    coroutines.append(fill_orbit_with_garbage(canvas))

    # obstacles_list = show_obstacles(canvas, obstacles)
    # coroutines.append(obstacles_list)

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
