import curses
import utils


async def blink(canvas, row, column, symbol='*', waiting_time=10):
    stars = ((curses.A_DIM, 2), (0, 0.3), (curses.A_BOLD, 0.5), (0, 0.3))

    await utils.wait_time(waiting_time)

    while True:
        for text_attrs, time_for_sleep in stars:
            canvas.addstr(row, column, symbol, text_attrs)
            await utils.wait_time(time_for_sleep * 10)
