import random
import curses

import utils
from sprites import blink, fire
from sprites.rocket_sprite import space_ship
from settings import SPACESHIP_SPEED, STARS_COUNT, FIRE_SPEED


def get_stars(canvas):
    stars = []
    max_y, max_x = utils.get_terminal_size()
    for _ in range(0, STARS_COUNT):
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
    curses.update_lines_cols()

    coroutines = []
    fire_animation = get_fire(canvas)
    coroutines.append(fire_animation)

    stars = get_stars(canvas)
    coroutines += stars
    rocket_animation = space_ship(
        canvas, [rocket_frame_1, rocket_frame_2], SPACESHIP_SPEED
    )
    coroutines.append(rocket_animation)

    while True:
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)
            if len(coroutines) == 0:
                break
            utils.prepare_draw(canvas)


if __name__ == '__main__':
    try:
        rocket_frame_1 = utils.get_rocket_flame_1()
        rocket_frame_2 = utils.get_rocket_flame_2()
    except FileNotFoundError as e:
        print(f'Not found "{e.filename}"')
        exit()
    curses.update_lines_cols()
    curses.wrapper(main, rocket_frame_1, rocket_frame_2)
