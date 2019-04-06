import curses


def get_canvas():
    canvas = curses.initscr()
    return canvas


def get_terminal_size():
    canvas = get_canvas()
    max_y, max_x = canvas.getmaxyx()
    return max_y, max_x
