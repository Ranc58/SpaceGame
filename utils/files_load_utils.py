from settings import (
    ROCKET_FILE_1_PATH,
    ROCKET_FILE_2_PATH,
    TRASH_LARGE_FILE,
    TRASH_SMALL_FILE,
    DUCK_FILE,
    LAMP_FILE,
    TRASH_XL_FILE,
    HUBBLE_FILE,
    GAMEOVER_FILE,
)


def get_rocket_flame_1():
    with open(ROCKET_FILE_1_PATH) as f:
        return f.read()


def get_rocket_flame_2():
    with open(ROCKET_FILE_2_PATH) as f:
        return f.read()


def get_trash_large():
    with open(TRASH_LARGE_FILE) as trash_file:
        return trash_file.read()


def get_trash_small():
    with open(TRASH_SMALL_FILE) as trash_file:
        return trash_file.read()


def get_trash_xl():
    with open(TRASH_XL_FILE) as trash_file:
        return trash_file.read()


def get_duck():
    with open(DUCK_FILE) as duck:
        return duck.read()


def get_hubble():
    with open(HUBBLE_FILE) as hubble:
        return hubble.read()


def get_lamp():
    with open(LAMP_FILE) as lamp:
        return lamp.read()


def get_gameover():
    with open(GAMEOVER_FILE) as gameover:
        return gameover.read()
