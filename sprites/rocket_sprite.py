import asyncio

import utils


async def space_ship(canvas, base_rocket, rockets):
    max_y, max_x = utils.get_terminal_size()
    while True:

        for rocket in rockets:

            utils.draw_frame(canvas, max_y-10, max_x/2, base_rocket)
            utils.draw_frame(canvas, max_y-5, max_x/2, rocket)
            canvas.refresh()
            await asyncio.sleep(0)
            utils.draw_frame(canvas, max_y-5, max_x/2, rocket, negative=True)


