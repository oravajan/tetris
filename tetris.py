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
        super(PauseMenu, self).__init__('Pause', background)

        pos = self.title_text.y - FONT_SIZE_TITLE // 2 + FONT_SIZE_MENU_ITEM // 2
        self.items.append(MenuItem('Resume', pos - MENU_ITEMS_OFFSET, start_game))
        self.items.append(MenuItem('Save Game', pos - 2*MENU_ITEMS_OFFSET, None))
        self.items.append(MenuItem('Exit to Main menu', pos - 3*MENU_ITEMS_OFFSET, pyglet.app.exit))
        self.reset()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GRID CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Grid:
    def __init__(self, tile_size, width, height):
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.x = WINDOW_WIDTH // 2 - (width * tile_size) // 2

    def draw(self):
        x = self.x
        for cols in range(self.width + 1):
            pyglet.shapes.Line(x, 0, x, WINDOW_HEIGHT).draw()
            x += self.tile_size

        y = 0
        for rows in range(self.height + 1):
            pyglet.shapes.Line(self.x, y, self.x + self.width * self.tile_size, y).draw()
            y += self.tile_size


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GAME CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Game:
    def __init__(self):
        self.running = False
        self.grid = Grid(TILE_SIZE, PLAY_GRID_WIDTH, PLAY_GRID_HEIGHT)

    def run(self):
        self.running = True
        pyglet.clock.schedule_interval(self.update, 1 / FREQ)

    def update(self, dt):
        pass

    def draw(self):
        self.grid.draw()

    def on_key_press(self, symbol, modifiers):
        global overlay
        if symbol == key.Q:
            self.running = False
            pyglet.clock.unschedule(self.update)
            overlay = PauseMenu(pyglet.resource.image("background.png"))
            return True

    def is_running(self):
        return self.running


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN FUNCTION                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def main():
    global overlay, game
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    try:
        tetris_img_grid = pyglet.image.ImageGrid(pyglet.resource.image("blocks.png"), 1, 5)
        overlay = MainMenu(pyglet.resource.image("background.png"))
        window.set_icon(pyglet.resource.image("tetris_icon.ico"))
    except pyglet.resource.ResourceNotFoundException as error:
        print(error)
        exit(-1)
    else:
        pyglet.app.run()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 FUNCTIONS                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
def start_game():
    global overlay
    del overlay
    overlay = None
    game.run()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GLOBAL VARIABLES                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
window_x = (pyglet.canvas.Display().get_screens()[0].width - window.width) // 2
window_y = (pyglet.canvas.Display().get_screens()[0].height - window.height) // 2
window.set_location(window_x, window_y)
overlay = Overlay()
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
