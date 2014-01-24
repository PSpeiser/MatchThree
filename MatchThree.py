import pygame, sys
from pygame.locals import *
import random
# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
# set up the window
windowSurface = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('MatchThree')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
VIOLET = (143, 0, 255)
ORANGE = (255, 165, 0)
COLORS = (RED, BLUE, GREEN, YELLOW, VIOLET, ORANGE, WHITE)
# set up fonts
basicFont = pygame.font.SysFont(None, 48)
SQUARE_SIZE = 60
BORDER_WIDTH = 10
MOVE_SPEED = 5


class Cell(object):
    def __init__(self, row, column):
        self.row = -8 + row
        self.column = column
        self.x_offset = 0
        self.y_offset = 0
        self.color = random.choice(COLORS)
        self.selected = False
        self.go_to(row, column)

    def draw(self, surface):
        top = self.row * SQUARE_SIZE + self.y_offset
        left = self.column * SQUARE_SIZE + self.x_offset
        if self.selected:
            pygame.draw.rect(surface, RED,
                             Rect(left, top, SQUARE_SIZE + BORDER_WIDTH / 2, SQUARE_SIZE + BORDER_WIDTH / 2))

        rect = Rect(left + BORDER_WIDTH / 2, top + BORDER_WIDTH / 2, SQUARE_SIZE - BORDER_WIDTH / 2,
                    SQUARE_SIZE - BORDER_WIDTH / 2)
        pygame.draw.rect(surface, self.color, rect)

    def update(self):
        if self.x_offset != 0:
            if self.x_offset > 0:
                self.x_offset -= MOVE_SPEED
            else:
                self.x_offset += MOVE_SPEED
        if self.y_offset != 0:
            if self.y_offset > 0:
                self.y_offset -= MOVE_SPEED
            else:
                self.y_offset += MOVE_SPEED

    def go_to(self, row, column):
        if self.row == row and self.column == column:
            self.x_offset = 0
            self.y_offset = 0
        elif self.row == row:
            self.x_offset = (self.column - column) * SQUARE_SIZE
            self.y_offset = 0
            self.column = column
        elif self.column == column:
            self.x_offset = 0
            self.y_offset = (self.row - row) * SQUARE_SIZE
            self.row = row

    def swap_with(self, other):
        temp_row = other.row
        temp_column = other.column
        other.go_to(self.row, self.column)
        self.go_to(temp_row, temp_column)


class Board(object):
    def __init__(self):
        self.cells = []
        for row in range(0, 8, 1):
            for column in range(0, 8, 1):
                self.cells.append(Cell(row, column))

    def fill(self):
        matrix = self.to_matrix()

    def to_matrix(self):
        matrix = [[()] * 8] * 8
        for cell in self.cells:
            matrix[cell.row][cell.column] = cell
        return matrix

    def draw(self, surface):
        for cell in self.cells:
            cell.draw(surface)

    def update(self):
        for cell in self.cells:
            cell.update()

    def get_cell(self, row, column):
        for cell in self.cells:
            if cell.row == row and cell.column == column:
                return cell


selected = None
board = Board()
# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            column = event.pos[0] / SQUARE_SIZE
            row = event.pos[1] / SQUARE_SIZE
            cell = board.get_cell(row, column)
            if cell == selected:
                cell.selected = False
                selected = None
            else:
                if selected is not None:
                    if cell.row == selected.row and abs(cell.column - selected.column) == 1 or \
                                            cell.column == selected.column and abs(cell.row - selected.row) == 1:
                        cell.swap_with(selected)
                        selected.selected = False
                        selected = None
                else:
                    selected = cell
                    cell.selected = True

    board.update()

    windowSurface.fill(BLACK)
    board.draw(windowSurface)
    pygame.display.update()
    mainClock.tick(60)