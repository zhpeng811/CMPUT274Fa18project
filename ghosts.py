# -------------------------------
# Names: Meilin Lyu, Ze Hui Peng
# ID #s: 1577829, 1594884
# CMPUT 274 Fall 2018
# Final Project: Pacman Arcade Game
# -------------------------------

import pygame
import random


class ghosts():
    """
    Class Description: the ghost object that will collide with pacman in
    the game.
    """
    def __init__(self, row, column, name, pacmap, direction):
        """
        Description: initialize all stats for the ghost object.
        """
        # initial start position for the ghost
        self.row = row
        self.column = column
        # size of the ghost
        self.blockwidth = 30
        self.blockheight = 30

        self.name = name
        self.pacghostsImg = pygame.image.load("images/"+self.name+".png")
        self.pacghostsImg = pygame.transform.scale(self.pacghostsImg, (30, 30))
        self.m = pacmap
        self.direction = direction
        self.time = 0

    def draw(self, screen):
        """
        Description: draw the ghosts on the screen
        """
        screen.blit(self.pacghostsImg, ((self.column)*self.blockwidth,
                                        (self.row)*self.blockheight))

    def move(self, pacman, mode):
        """
        Description: allow the ghost to move based on the algorithm, the
        algorithum is chosen by the argument mode.
        Args: pacman(object): the pacman object, the chase algoritum need the
        position of pacman to calculate the "Manhattan Distance"(vertical and
        horizontal distances seperately).
              mode(int): an integer number between 1 to 3
              1 = chase mode
              2 = random mode
              3 = pattern mode
        """
        self.time += 1
        # it will move once for every ten times that this function is called
        if self.time == 10:
            self.time = 0
            if self.direction == "right":
                if mode == 1 and self.m[self.row][self.column+1] != "#":
                    # the orange ghost could cross the inner walls but
                    # not the outer walls
                    self.column += 1
                    self.chase(pacman)

                elif mode != 1:
                    if self.m[self.row][self.column+1] == "1" or \
                       self.m[self.row][self.column+1] == "O":
                        # the other 3 ghosts could move right
                        # if there is road on its right
                        self.column += 1
                    if mode == 2:
                        self.changeDirection()
                    elif mode == 3:
                        # the blue ghost would movedown when it is on the 15th
                        # column,1st row(move with pattern)
                        if self.column == 15:
                            self.direction = "down"

            elif self.direction == "left":
                if mode == 1 and self.m[self.row][self.column-1] != "#":
                    # the orange ghost could cross the inner walls but
                    # not the outer walls
                    self.column -= 1
                    self.chase(pacman)
                elif mode != 1:
                    if self.m[self.row][self.column-1] == "1" or \
                       self.m[self.row][self.column-1] == "O":
                        # the other 3 ghosts could move left if
                        # there is road on its left
                        self.column -= 1
                    if mode == 2:
                        # two ghosts would move randomly
                        self.changeDirection()
                    elif mode == 3:
                        # the blue ghost would move upward when it is
                        # on the 1st column, 7th row(move with pattern)
                        if self.column == 1:
                            self.direction = "up"

            elif self.direction == "up":
                if mode == 1 and self.m[self.row-1][self.column] != "#":
                    # the orange ghost could cross the inner walls but
                    # not the outer walls
                    self.row -= 1
                    self.chase(pacman)
                elif mode != 1:
                    if self.m[self.row-1][self.column] == "1" or \
                       self.m[self.row-1][self.column] == "O":
                        # the other 3 ghosts could move upward if
                        # there is road on the top
                        self.row -= 1
                    if mode == 2:
                        # two ghosts would move randomly
                        self.changeDirection()
                    elif mode == 3:
                        if self.row == 1:
                            # the blue ghost would move to right when it is
                            # on the 1st row,1st column
                            self.direction = "right"

            elif self.direction == "down":
                if mode == 1 and self.m[self.row+1][self.column] != "#":
                    # the orange ghost could cross the inner walls but
                    # not the outer walls
                    self.row += 1
                    self.chase(pacman)
                elif mode != 1:
                    # the other 3 ghosts could move downward
                    # if there is road under itself
                    if self.m[self.row+1][self.column] == "1" or \
                       self.m[self.row+1][self.column] == "O":
                        self.row += 1
                    if mode == 2:
                        # two ghosts would move randomly
                        self.changeDirection()
                    elif mode == 3:
                        if self.row == 7:
                            # the blue ghost would move ot left when
                            # it is on the 15th column,7th row
                            self.direction = "left"

    def chase(self, pacman):
        """
        Description: set the chase mode for the orange ghost with algorithm
        """
        # idea from Morning Problem "Manhattan Distance"

        distH = abs(self.column - pacman.col)
        # the horizontal distance between ghost and pacman
        distV = abs(self.row - pacman.row)
        # the vertical distance between ghost and pacman
        if distH > distV:
            # if the ghost is more close to pacman vertically
            # it moves horizontally
            if self.column > pacman.col:
                # if the ghost is on the right of the pacman, chase left
                self.direction = "left"
            elif self.column < pacman.col:
                # if the ghost is on the left of the pacman, chase right
                self.direction = "right"
        else:
            # if the ghosts is more close to pacman horizontally
            # (or the horizontal and vertical distance are equal),
            # it will move vertically
            if self.row < pacman.row:
                # if the ghost is above the pacman,move downward
                self.direction = "down"
            elif self.row > pacman.row:
                # if the ghost is under the pacman, move upward
                self.direction = "up"

    def changeDirection(self):
        """
        Description: pick a random direction for the ghost to move.
        """
        r = random.randint(0, 3)
        # a random direction will be chosen using the random module
        if r == 0:
            self.direction = "right"
        elif r == 1:
            self.direction = "left"
        elif r == 2:
            self.direction = "up"
        elif r == 3:
            self.direction = "down"
