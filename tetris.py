# Simple tetris game using pyglet lib
# By Jan Orava

import pyglet


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CONSTANT DECLARATION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
TILE_SIZE = 30
PLAY_GRID_WIDTH = 10
PLAY_GRID_HEIGHT = 20

WINDOW_WIDTH = PLAY_GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = PLAY_GRID_HEIGHT * TILE_SIZE
WINDOW_TITLE = "Tetris"
game_window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 WINDOW EVENTS                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
@game_window.event
def on_draw():
    game_window.clear()
    test.draw()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 START GAME                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()
    test = pyglet.sprite.Sprite(img=pyglet.resource.image("blocks.png"), x=0, y=0)
    pyglet.app.run()
