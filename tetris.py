# Simple tetris game using pyglet lib
# By Jan Orava

import pyglet
from pyglet.window import key

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CONSTANT DECLARATION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
TILE_SIZE = 30
PLAY_GRID_WIDTH = 10
PLAY_GRID_HEIGHT = 20

WINDOW_WIDTH = PLAY_GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = PLAY_GRID_HEIGHT * TILE_SIZE
WINDOW_TITLE = "Tetris"


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MENU CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Overlay:
    def draw(self):
        pass


class Menu(Overlay):
    def __init__(self, title):
        self.items = []
        self.title_text = pyglet.text.Label(title,
                                            font_name='Verdana',
                                            font_size=36,
                                            x=WINDOW_WIDTH // 2,
                                            y=350,
                                            anchor_x='center',
                                            anchor_y='center')
        self.selected_index = 0

    def reset(self):
        self.selected_index = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.DOWN:
            self.selected_index += 1
        elif symbol == key.UP:
            self.selected_index -= 1
        elif symbol == key.ENTER:
            self.items[self.selected_index].on_key_press(symbol, modifiers)

        if self.selected_index > len(self.items) - 1:
            self.selected_index = 0
        if self.selected_index < 0:
            self.selected_index = len(self.items) - 1

    def draw(self):
        self.title_text.draw()
        for index, item in enumerate(self.items):
            if index == self.selected_index:
                item.draw(True)
            else:
                item.draw(False)


class MenuItem:
    def __init__(self, label, y, activate_func):
        self.text = pyglet.text.Label(label,
                                      font_name='Verdana',
                                      font_size=14,
                                      x=WINDOW_WIDTH // 2,
                                      y=y,
                                      anchor_x='center',
                                      anchor_y='center')
        self.activate_func = activate_func

    def draw(self, selected):
        if selected:
            self.text.color = (255, 0, 0, 255)
        else:
            self.text.color = (255, 255, 255, 255)
        self.text.draw()

    def on_key_press(self, symbol, modifiers):
        if self.activate_func:
            self.activate_func()


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Tetris')

        self.items.append(MenuItem('New Game', 240, None))
        self.items.append(MenuItem('Load Game', 200, None))
        self.items.append(MenuItem('Leaderboard', 160, None))
        self.items.append(MenuItem('Quit Game', 120, pyglet.app.exit))
        self.reset()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN FUNCTION                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def main():
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    try:
        img = pyglet.resource.image("blocks.png")
    except pyglet.resource.ResourceNotFoundException as error:
        print(error)
        exit(-1)
    else:
        tetris_img_grid = pyglet.image.ImageGrid(img, 1, 5)
        pyglet.app.run()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GLOBAL VARIABLES                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
game_window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
overlay = MainMenu()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 WINDOW EVENTS                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
@game_window.event
def on_draw():
    game_window.clear()
    overlay.draw()


@game_window.event
def on_key_press(symbol, modifiers):
    overlay.on_key_press(symbol, modifiers)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 START GAME                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
