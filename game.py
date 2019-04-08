import time
import random
import curses

import utils
from sprites import blink, fire
from sprites.rocket_sprite import get_spaceship
from settings import SPACESHIP_SPEED, STARS_COUNT, FIRE_SPEED, TIC_TIMEOUT


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


def main(canvas, rocket_frame_1, rocket_frame_2):
    curses.curs_set(False)
    canvas.border()
    coroutines = []
    fire_animation = get_fire(canvas)
    coroutines.append(fire_animation)

    stars = get_stars(canvas, STARS_COUNT)
    coroutines += stars
    spaceship = get_spaceship(
        canvas, [rocket_frame_1, rocket_frame_2], SPACESHIP_SPEED
    )
    coroutines.append(spaceship)

    while True:
        for coro in coroutines:
            try:
                coro.send(None)

            except StopIteration:
                coroutines.remove(coro)
            if len(coroutines) == 0:
                break
            canvas.refresh()
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
