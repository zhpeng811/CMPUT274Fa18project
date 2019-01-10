# -------------------------------
# Names: Meilin Lyu, Ze Hui Peng
# ID #s: 1577829, 1594884
# CMPUT 274 Fall 2018
# Final Project: Pacman Arcade Game
# -------------------------------

import pygame


class Pacman:
    """
    Class Description: the pacman object that will eat pacdots and collide with
    the ghosts in the game.
    """
    def __init__(self, row, column, pacmap, direction, name):
        """
        Description: initialize all stats for the pacman object.
        """
        # initial start position for the pacman
        self.row = row
        self.col = column

        # size of the pacman
        self.width = 30
        self.height = 30

        self.name = name
        # load pictures
        self.Img = pygame.image.load("images/"+self.name+'_right.jpg')
        self.Img = pygame.transform.scale(self.Img, (self.width, self.height))
        self.m = pacmap
        # at the beginning, the pacman start with a score of 10
        self.score = 10
        self.direction = direction

    def draw(self, screen):
        """
        Description: draw the pacman on the screen
        Args : screen(object): the main display screen initialized using
        pygame.display.set_mode
        """
        screen.blit(self.Img, ((self.col)*self.width, (self.row)*self.height))

    def eat_pacdot(self):
        """
        Description: change the pacmap and add score to pacman when a pacdot
        is eaten by pacman.
        """
        if self.m[self.row][self.col] == "1":
            # if pacman eat a pacdot, change the "1" in pacmap to a "O"
            self.m[self.row][self.col] = "O"
            self.score += 10
            # play the sound effect when a pacdot is eaten
            sound = pygame.mixer.Sound("music/pacman_eatdot.wav")
            sound.play()

    def Left(self):
        """
        Description: pacman will move to the left one unit(if the left path is
        not a wall) each time this function is called.
        """
        if self.m[self.row][self.col - 1] != "X" and \
           self.m[self.row][self.col - 1] != "#":
            self.col -= 1
        # pacman could move to left if there is no wall on the left of itself

        self.Img = pygame.image.load("images/"+self.name+'_left.jpg')
        # the pacman turns its head to the left if it goes to left
        self.Img = pygame.transform.scale(self.Img, (self.width, self.height))

    def Right(self):
        """
        Description: pacman will move to the right one unit(if the right path
        is not a wall) each time this function is called.
        """
        if self.m[self.row][self.col+1] != "X" and \
           self.m[self.row][self.col + 1] != "#":
            self.col += 1
        #  pacman can move to right if there is no wall on the right of itself
        self.Img = pygame.image.load("images/" + self.name + '_right.jpg')
        #  the pacman turns its head to the right if it goes to right
        self.Img = pygame.transform.scale(self.Img, (self.width, self.height))

    def Up(self):
        """
        Description: pacman will move up one unit(if the above path is
        not a wall) each time this function is called.
        """
        if self.m[self.row - 1][self.col] != "X" and\
           self.m[self.row-1][self.col] != "#":
            self.row -= 1
            #  pacman could move upward if there is no wall on top of itself

        self.Img = pygame.image.load("images/"+self.name+'_up.jpg')
        #  the pacman turns its head up if it goes upward
        self.Img = pygame.transform.scale(self.Img, (self.width, self.height))

    def Down(self):
        """
        Description: pacman will move down one unit(if the below path is
        not a wall) each time this function is called.
        """
        if self.m[self.row+1][self.col] != "X" and \
           self.m[self.row+1][self.col] != "#":
            self.row += 1
            # pacman could move down if there is no wall below itself

        self.Img = pygame.image.load("images/"+self.name+'_down.jpg')
        # the pacman turn its head down if it goes downward
        self.Img = pygame.transform.scale(self.Img, (self.width, self.height))

    def dodge(self, ghost, name):
        """
        Descrption: pacman trying to dodge(run away) from the ghosts,
        it's score will reduce upon collision.
        Args: ghost(object): this function requires the current postion of
        the each ghost object.
              name(str): the name for the ghost object
        """
        # if the orange ghost collides with pacman, the score will turns to 0
        # (pacman immediately lose the game)
        if self.row == ghost.row and self.col == ghost.column:
            if ghost.name == "orange":
                self.score = 0
            else:
                #  if other ghosts collide with pacman, the score will be
                #  reduced by 100 for each game tick of the collision
                self.score = -100

    def chase(self, ghost):
        """
        Descrption: pacman trying to chase(eat) the ghosts, ghost will no
        longer display onto the screen if pacman eat that ghost.
        Args: ghost(object): this function requires the current postion of
        the each ghost object.
        """
        if self.row == ghost.row and self.col == ghost.column:
            return(True)
        else:
            return(False)
