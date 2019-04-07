import random
import curses
import time

import utils
from sprites import blink, fire
from sprites.rocket_sprite import space_ship


def get_stars():
    stars = []
    max_y, max_x = utils.get_terminal_size()
    for _ in range(0, 100):
        symbol = random.choice('+*.:')
        y_coord = random.randint(1, max_y - 1)
        x_coord = random.randint(1, max_x - 1)
        star = curses.wrapper(blink, y_coord, x_coord, symbol)
        stars.append(star)
    return stars


def get_fire():
    max_y, max_x = utils.get_terminal_size()
    return fire(canvas, max_y - 5, round(max_x / 2), rows_speed=-2)


if __name__ == '__main__':
    curses.update_lines_cols()

    coroutines = get_stars()
    canvas = utils.get_canvas()
    fire_animation = get_fire()
    coroutines.append(fire_animation)
    main_rocket = utils.get_rocket_main()
    rocket_frame_1 = utils.get_rocket_flame_1()
    rocket_frame_2 = utils.get_rocket_flame_2()
    rocket_animation = space_ship(canvas, main_rocket, [rocket_frame_1, rocket_frame_2])
    coroutines.append(rocket_animation)

    while True:
        for coro in coroutines:
            try:
                curses.curs_set(False)
                coro.send(None)
                canvas.border()
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coro)
            if len(coroutines) == 0:
                break
