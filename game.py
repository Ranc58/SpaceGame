import time
import curses


def draw(canvas):
    row, column = (7, 20)
    canvas.addstr(row, column, 'Hello, World!',curses.A_BLINK)
    canvas.border()
    canvas.refresh()
    time.sleep(6)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
