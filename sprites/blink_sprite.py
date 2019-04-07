import curses
import asyncio

import utils


async def blink(canvas, row, column, symbol='*'):
    stars = ((curses.A_DIM, 2), (0, 0.3), (curses.A_BOLD, 0.5), (0, 0.3))
    while True:
        for star in stars:
            text_type = star[0]
            time_for_sleep = star[1]
            iterations_count = 0
            needles_count = utils.convert_ms_to_iterations(time_for_sleep)
            for _ in reversed(range(0, int(needles_count) + 1)):
                if iterations_count == 0:
                    canvas.addstr(row, column, symbol, text_type)
                    await asyncio.sleep(0)
                iterations_count -= 1
