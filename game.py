import _curses

import sys
import time
import random
import curses

import utils
from sprites import blink, fire
from sprites.trash_sprite import fly_garbage
from sprites.rocket_sprite import animate_spaceship, run_spaceship
from settings import STARS_COUNT, FIRE_SPEED, TIC_TIMEOUT, CHANGE_YEAR_DELAY
from global_vars import coroutines, year, obstacles


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
    return fly_garbage(canvas, column_for_trash, trash_frame)


async def fill_orbit_with_garbage(canvas):
    global coroutines
    global obstacles
    global year
    while True:
        current_year = year.get('current_year')
        await_time = utils.get_garbage_delay_tics(current_year)
        await utils.wait_time(await_time)
        garbage = get_trash(canvas)
        coroutines.append(garbage)


async def change_year_data(canvas):
    global year
    max_y, max_x = utils.get_terminal_size()

    while True:
        current_year = year.get('current_year')
        previous_message = utils.get_message(current_year-1)
        utils.draw_frame(canvas, round(max_y - 2), round(2), str(previous_message), negative=True)
        message = utils.get_message(current_year)
        utils.draw_frame(canvas, round(max_y - 2), round(2), str(message))
        if current_year == 1961:
            orbit_with_garbage = fill_orbit_with_garbage(canvas)
            coroutines.append(orbit_with_garbage)
        if current_year == 2020:
            fire_animation = get_fire(canvas)
            coroutines.append(fire_animation)
        await utils.wait_time(CHANGE_YEAR_DELAY)
        year['current_year'] += 1


def main(canvas, rocket_frame_1, rocket_frame_2):
    global coroutines
    global year

    curses.curs_set(False)
    year_change = change_year_data(canvas)
    coroutines.append(year_change)
    spaceship_frame = animate_spaceship([rocket_frame_1, rocket_frame_2])
    coroutines.append(spaceship_frame)

    spaceship = run_spaceship(canvas)
    coroutines.append(spaceship)

    stars = get_stars(canvas, STARS_COUNT)
    coroutines += stars

    while True:
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)
            except _curses.error:
                continue
            utils.refresh_draw(canvas)
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    try:
        rocket_frame_1 = utils.get_rocket_flame_1()
        rocket_frame_2 = utils.get_rocket_flame_2()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    curses.update_lines_cols()
    curses.wrapper(main, rocket_frame_1, rocket_frame_2)
