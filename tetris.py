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

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Tetris"

WINDOW_OFFSET = 5

FONT_SIZE_TITLE = 36
FONT_SIZE_MENU_ITEM = 14
FONT_NAME = 'Algerian'
MENU_ITEMS_OFFSET = 40

BACKGROUND_IMG = pyglet.image
ICON = pyglet.image


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
                                            font_name=FONT_NAME,
                                            font_size=FONT_SIZE_TITLE,
                                            x=WINDOW_WIDTH // 2,
                                            y=WINDOW_HEIGHT * 0.7,
                                            color=(0, 255, 120, 255),
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
                                      font_name=FONT_NAME,
                                      font_size=FONT_SIZE_MENU_ITEM,
                                      x=WINDOW_WIDTH // 2,
                                      y=y,
                                      anchor_x='center',
                                      anchor_y='center')
        self.activate_func = activate_func

    def draw(self, selected):
        if selected:
            self.text.color = (0, 255, 220, 255)
        else:
            self.text.color = (255, 255, 255, 255)
        self.text.draw()

    def on_key_press(self, symbol, modifiers):
        if self.activate_func:
            self.activate_func()


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Tetris')

        pos = self.title_text.y - FONT_SIZE_TITLE // 2 + FONT_SIZE_MENU_ITEM // 2
        self.items.append(MenuItem('New Game', pos - MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Load Game', pos - 2*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Leaderboard', pos - 3*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Quit Game', pos - 4*MENU_ITEMS_OFFSET, pyglet.app.exit))
        self.reset()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN FUNCTION                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def main():
    global BACKGROUND_IMG, ICON
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    try:
        img = pyglet.resource.image("blocks.png")
        BACKGROUND_IMG = pyglet.resource.image("background.png")
        ICON = pyglet.resource.image("tetris_icon.ico")
    except pyglet.resource.ResourceNotFoundException as error:
        print(error)
        exit(-1)
    else:
        tetris_img_grid = pyglet.image.ImageGrid(img, 1, 5)
        window.set_icon(ICON)
        pyglet.app.run()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GLOBAL VARIABLES                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
window_x = (pyglet.canvas.Display().get_screens()[0].width - window.width) // 2
window_y = (pyglet.canvas.Display().get_screens()[0].height - window.height) // 2
window.set_location(window_x, window_y)
overlay = MainMenu()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 WINDOW EVENTS                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
@window.event
def on_draw():
    window.clear()
    BACKGROUND_IMG.blit(0, 0)

    if overlay:
        overlay.draw()


@window.event
def on_key_press(symbol, modifiers):
    overlay.on_key_press(symbol, modifiers)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 START GAME                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
