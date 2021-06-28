# Simple tetris game using pyglet lib
# By Jan Orava

import random
import pyglet
from pyglet.window import key

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CONSTANT DECLARATION                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
TILE_SIZE = 30
PLAY_GRID_WIDTH = 10
PLAY_GRID_HEIGHT = 20

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Tetris"

WINDOW_OFFSET = 5

FONT_SIZE_TITLE = 36
FONT_SIZE_MENU_ITEM = 14
FONT_NAME = 'Algerian'
MENU_ITEMS_OFFSET = 40
GAME_SPEED = 2.0

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()


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
    def __init__(self, x, y):
        self.grid_start_x = x
        self.grid_start_y = y
        self.type = random.randint(0, 6)
        self.type = 0
        if self.type == 0:
            self.shape = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [1, 1, 1, 1],
                          [0, 0, 0, 0]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[0], 0, 0)
        elif self.type == 1:
            self.shape = [[0, 0, 0],
                          [0, 0, 1],
                          [1, 1, 1]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[1], 0, 0)
        elif self.type == 2:
            self.shape = [[0, 0, 0],
                          [1, 0, 0],
                          [1, 1, 1]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[2], 0, 0)
        elif self.type == 3:
            self.shape = [[0, 0, 0],
                          [0, 1, 1],
                          [1, 1, 0]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[3], 0, 0)
        elif self.type == 4:
            self.shape = [[0, 0, 0],
                          [1, 1, 0],
                          [0, 1, 1]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[4], 0, 0)
        elif self.type == 5:
            self.shape = [[0, 0, 0],
                          [0, 1, 0],
                          [1, 1, 1]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[5], 0, 0)
        elif self.type == 6:
            self.shape = [[1, 1],
                          [1, 1]]
            self.img = pyglet.sprite.Sprite(tetris_img_grid[6], 0, 0)

        self.x = PLAY_GRID_WIDTH // 2 - len(self.shape) // 2
        self.y = PLAY_GRID_HEIGHT - 2

    def draw(self):
        x = self.x
        y = self.y
        for row, e in reversed(list(enumerate(self.shape))):
            for col in range(len(self.shape[row])):
                self.img.x = x * (TILE_SIZE + 1) + self.grid_start_x
                self.img.y = y * (TILE_SIZE + 1) + self.grid_start_y
                if self.shape[row][col] == 1:
                    self.img.draw()
                else:
                    pyglet.shapes.Rectangle(x * (TILE_SIZE + 1) + self.grid_start_x,
                                            y * (TILE_SIZE + 1) + self.grid_start_y,
                                            TILE_SIZE, TILE_SIZE, (165, 42, 42)).draw()
                x += 1
            y += 1
            x = self.x

    def move_left(self, grid):
        x = self.x
        for col in range(len(self.shape[0])):
            for row in range(len(self.shape)):
                if self.shape[row][col] == 1:
                    x += col
                    break
            else:
                # Continue if the inner loop wasn't broken.
                continue
            break

        # if x >= 1 and grid.data[self.y][x - 1] == 0:
        if grid.is_free(self.shape, self.x - 1, self.y):
            self.x -= 1

    def move_right(self, grid):
        x = self.x
        for col in reversed(range(len(self.shape[0]))):
            for row in range(len(self.shape)):
                if self.shape[row][col] == 1:
                    x += col
                    break
            else:
                # Continue if the inner loop wasn't broken.
                continue
            break

        # if x < PLAY_GRID_WIDTH - 1 and grid.data[self.y][x + 1] == 0:
        if grid.is_free(self.shape, self.x + 1, self.y):
            self.x += 1

    def move_down(self, grid):
        y = self.y
        for index, row in reversed(list(enumerate(self.shape))):
            if row.count(1) > 0:
                y += len(self.shape) - index - 1
                break

        if grid.is_free(self.shape, self.x, self.y - 1):
            self.y -= 1
            return True
        return False

    def turn_over(self, grid):
        tmp = []
        for row in range(len(self.shape)):
            tmp.append([])
            for col in range(len(self.shape[0])):
                tmp[row].append(0)

        for row in range(len(self.shape)):
            for col in range(len(self.shape[0])):
                if self.shape[row][col] == 1:
                    tmp[col][len(self.shape) - 1 - row] = 1
        if grid.is_free(tmp, self.x, self.y):
            self.shape = tmp


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GRID CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Grid:
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

        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col] == 1:
                    pyglet.shapes.Rectangle(self.start_x + col * (TILE_SIZE+1),
                                            self.start_y + row * (TILE_SIZE+1),
                                            TILE_SIZE, TILE_SIZE,
                                            (255, 0, 0)).draw()

    def reset(self):
        self.data.clear()
        for row in range(self.height):
            self.data.append([])
            for col in range(self.width):
                self.data[row].append(0)

    def is_free(self, shape, x, y):
        for row in reversed(range(len(shape))):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    if len(shape) - 1 - row + y < 0 or len(shape) - 1 - row + y > self.height - 1:
                        return False
                    if col + x < 0 or col + x > self.width - 1:
                        return False
                    if self.data[len(shape) - 1 - row + y][col + x] == 1:
                        return False
        return True


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GAME CLASS                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class Game:
    def __init__(self):
        self.running = False
        self.grid = Grid(TILE_SIZE, PLAY_GRID_WIDTH, PLAY_GRID_HEIGHT,
                         WINDOW_WIDTH // 2 - (PLAY_GRID_WIDTH * (TILE_SIZE+1) + 1) // 2,
                         WINDOW_OFFSET)
        self.block = Block(self.grid.start_x, self.grid.start_y)

    def run(self):
        self.unpause()

    def update(self, dt):
        if not self.block.move_down(self.grid):
            self.block = Block(self.grid.start_x, self.grid.start_y)

    def draw(self):
        self.grid.draw()
        self.block.draw()

    def pause(self):
        self.running = False
        pyglet.clock.unschedule(self.update)

    def unpause(self):
        self.running = True
        pyglet.clock.schedule_interval(self.update, 1 / GAME_SPEED)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pause_game()
        if symbol == key.LEFT:
            self.block.move_left(self.grid)
        if symbol == key.RIGHT:
            self.block.move_right(self.grid)
        if symbol == key.DOWN:
            self.block.y -= 1
        if symbol == key.UP:
            self.block.turn_over(self.grid)
        if symbol == key.P:
            pyglet.clock.unschedule(self.update)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 MAIN FUNCTION                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def main():
    global overlay

    overlay = main_menu
    window_x = (pyglet.canvas.Display().get_screens()[0].width - WINDOW_WIDTH) // 2
    window_y = (pyglet.canvas.Display().get_screens()[0].height - WINDOW_HEIGHT) // 2
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
    set_overlay(main_menu)


def pause_game():
    game.pause()
    set_overlay(pause_menu)


def unpause_game():
    game.unpause()
    set_clear_overlay()


def set_clear_overlay():
    set_overlay(None)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GLOBAL VARIABLES                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
try:
    main_menu = MainMenu(pyglet.resource.image("background.png"))
    pause_menu = PauseMenu(pyglet.resource.image("background.png"))
    window.set_icon(pyglet.resource.image("tetris_icon.ico"))
    tetris_img_grid = pyglet.image.ImageGrid(pyglet.resource.image("blocks.png"), 1, 7)
except pyglet.resource.ResourceNotFoundException as error:
    print(error)
    exit(-1)
overlay = Overlay()
game = Game()


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 WINDOW EVENTS                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
@window.event
def on_draw():
    window.clear()

    if game.running:
        game.draw()

    if overlay:
        overlay.draw()


@window.event
def on_key_press(symbol, modifiers):
    if overlay:
        overlay.on_key_press(symbol, modifiers)
    else:
        game.on_key_press(symbol, modifiers)
    return pyglet.event.EVENT_HANDLED


# -------------------------------------------------------------------------------------------------------------------- #
#                                                 START GAME                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
