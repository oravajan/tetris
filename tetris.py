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
FREQ = 60.0


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MENU CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Overlay:
    def draw(self):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def reset(self):
        pass


class Menu(Overlay):
    def __init__(self, title, background):
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
        self.background = background

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
        self.background.blit(0, 0)
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
    def __init__(self, background):
        super(MainMenu, self).__init__('Tetris', background)

        pos = self.title_text.y - FONT_SIZE_TITLE // 2 + FONT_SIZE_MENU_ITEM // 2
        self.items.append(MenuItem('New Game', pos - MENU_ITEMS_OFFSET, start_game))
        self.items.append(MenuItem('Load Game', pos - 2*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Leaderboard', pos - 3*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Quit Game', pos - 4*MENU_ITEMS_OFFSET, pyglet.app.exit))
        self.reset()


class PauseMenu(Menu):
    def __init__(self, background):
        super(PauseMenu, self).__init__('Paused', background)

        pos = self.title_text.y - FONT_SIZE_TITLE // 2 + FONT_SIZE_MENU_ITEM // 2
        self.items.append(MenuItem('Resume', pos - MENU_ITEMS_OFFSET, unpause_game))
        self.items.append(MenuItem('Save Game', pos - 2*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Exit to Main menu', pos - 3 * MENU_ITEMS_OFFSET, exit_game))
        self.reset()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 BLOCK CLASS                                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class Block:
    pass


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GRID CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Grid:
    # TODO 2D pole, 0=prazdno, 1=block,barva, predelat vykreslovani na urcitou pozici
    # TODO trida block, zvoleny block a dalsi na rade
    def __init__(self, tile_size, width, height, start_x, start_y):
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = self.start_x + self.width * (self.tile_size + 1)
        self.end_y = self.start_y + self.height * (self.tile_size + 1)
        self.data = []
        self.reset()

    def draw(self):
        x = self.start_x
        for cols in range(self.width + 1):
            pyglet.shapes.Line(x, self.start_y, x, self.end_y).draw()
            x += self.tile_size + 1

        y = self.start_y
        for rows in range(self.height + 1):
            pyglet.shapes.Line(self.start_x, y, self.end_x, y).draw()
            y += self.tile_size + 1

    def reset(self):
        self.data.clear()
        for row in range(self.height):
            tmp = []
            for col in range(self.width):
                tmp.append(0)
            self.data.append(tmp)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GAME CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Game:
    def __init__(self):
        self.running = False
        self.grid = Grid(TILE_SIZE, PLAY_GRID_WIDTH, PLAY_GRID_HEIGHT,
                         WINDOW_WIDTH // 2 - (PLAY_GRID_WIDTH * TILE_SIZE) // 2,
                         5 * WINDOW_OFFSET)

    def run(self):
        self.unpause()

    def update(self, dt):
        pass

    def draw(self):
        self.grid.draw()

    def pause(self):
        self.running = False
        pyglet.clock.unschedule(self.update)

    def unpause(self):
        self.running = True
        pyglet.clock.schedule_interval(self.update, 1 / FREQ)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q:
            pause_game()

    def is_running(self):
        return self.running


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN FUNCTION                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def main():
    global overlay, main_menu, pause_menu
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    try:
        tetris_img_grid = pyglet.image.ImageGrid(pyglet.resource.image("blocks.png"), 1, 5)
        main_menu = MainMenu(pyglet.resource.image("background.png"))
        pause_menu = PauseMenu(pyglet.resource.image("background.png"))
        window.set_icon(pyglet.resource.image("tetris_icon.ico"))
    except pyglet.resource.ResourceNotFoundException as error:
        print(error)
        exit(-1)
    else:
        overlay = main_menu
        window_x = (pyglet.canvas.Display().get_screens()[0].width - window.width) // 2
        window_y = (pyglet.canvas.Display().get_screens()[0].height - window.height) // 2
        window.set_location(window_x, window_y)
        pyglet.app.run()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 FUNCTIONS                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
def start_game():
    set_clear_overlay()
    game.run()


def set_overlay(new_overlay):
    global overlay
    overlay = new_overlay
    if overlay:
        overlay.reset()


def exit_game():
    global game
    del game
    game = Game()
    window.set_size(800, 600)
    set_overlay(main_menu)


def pause_game():
    game.pause()
    window.set_size(800, 600)
    set_overlay(pause_menu)


def unpause_game():
    game.unpause()
    set_clear_overlay()


def set_clear_overlay():
    window.set_size(800, 700)
    set_overlay(None)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GLOBAL VARIABLES                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
overlay = Overlay()
main_menu = None
pause_menu = None
game = Game()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 WINDOW EVENTS                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
@window.event
def on_draw():
    window.clear()

    if game.is_running():
        game.draw()

    if overlay:
        overlay.draw()


@window.event
def on_key_press(symbol, modifiers):
    if overlay:
        overlay.on_key_press(symbol, modifiers)
    else:
        game.on_key_press(symbol, modifiers)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 START GAME                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
