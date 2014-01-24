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
BLACK = (0,0,0)
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
MOVE_SPEED = 5

class Cell(object):
    def __init__(self,row,column):
        self.row = -8+row
        self.column = column
        self.x_offset = 0
        self.y_offset = 0
        self.color = random.choice(COLORS)
        self.go_to(row,column)

    def draw(self,surface):
        top = self.row * SQUARE_SIZE + self.y_offset
        left = self.column * SQUARE_SIZE + self.x_offset
        rect = Rect(left,top,SQUARE_SIZE,SQUARE_SIZE)
        pygame.draw.rect(surface,self.color,rect)

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

    def go_to(self,row,column):
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

    def swap_with(self,other):
        temp_row = self.row
        temp_column = self.column
        other.go_to(self.row,self.column)
        self.go_to(temp_row,temp_column)

class Board(object):
    def __init__(self):
        self.cells = []
        for row in range(0,8,1):
            for column in range(0,8,1):
                self.cells.append(Cell(row,column))
    def fill(self):
        matrix = self.to_matrix()

    def to_matrix(self):
        matrix = [[()]*8]*8
        for cell in self.cells:
            matrix[cell.row][cell.column] = cell
        return matrix
    def draw(self,surface):
        for cell in self.cells:
            cell.draw(surface)
    def update(self):
        for cell in self.cells:
            cell.update()


board = Board()
# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            pass

    board.update()

    windowSurface.fill(BLACK)
    board.draw(windowSurface)
    pygame.display.update()
    mainClock.tick(60)