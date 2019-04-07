import curses
import asyncio
import time

import utils


async def blink(canvas, row, column, symbol='*', waiting_time=10):
    stars = ((curses.A_DIM, 2), (0, 0.3), (curses.A_BOLD, 0.5), (0, 0.3))

    await utils.wait_time(waiting_time)

    while True:
        for star in stars:
            text_type = star[0]
            time_for_sleep = star[1]
            iterations_count = 0
            needles_count = utils.convert_ms_to_iterations(time_for_sleep * 1000)
            for _ in reversed(range(0, int(needles_count) + 1)):

                if iterations_count == 0:
                    time.sleep(0.001)
                    canvas.addstr(row, column, symbol, text_type)
                    await asyncio.sleep(0)
                iterations_count -= 1
            await utils.wait_time(time_for_sleep)
