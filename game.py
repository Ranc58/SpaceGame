import random
import curses

import utils
from sprites import blink, fire


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
