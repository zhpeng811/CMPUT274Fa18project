
import pygame
import random
from Pacman import *
from ghosts import *

# declared all below variables as global variables because it will be
# used in several functions

# global constants
display_width = 1050
display_height = 600
rect_width = 30
rect_height = 30

# global pacman map
pacman_map = []

# global game conditions
won = False
counter = 50
# 50s for one game
eaten = [False, False, False, False]


def setup():
    """ Description: initialize pygame and the display window """

    global screen
    pygame.init()
    pygame.font.init()
    # initialize the main display screen
    screen = pygame.display.set_mode((display_width, display_height), 0, 32)
    # set the caption title for the display window
    pygame.display.set_caption('CMPUT 274 Pacman Arcade Game')
    gameDisplay = pygame.display.set_mode((display_width, display_height))


def start_screen():
    """
    Description: the start screen window where player can choose which mode
    of the game they want to play.
    Returns: play(bool): return False if the quit button(on the top left hand
    corner) or the actual "Quit" button is pressed by the user,
    return True otherwise.
    """
    global screen, gamemode
    # initialize the size of the button and the xy coordinates to display
    button_width = 150
    button_height = 100
    buttons = []
    x1 = display_width/4
    x2 = display_width/1.8
    y1 = display_height/3
    y2 = display_height/1.5
    width = [x1, x2, x1, x2]
    height = [y1, y1, y2, y2]

    for i in range(0, 4):
        # set buttons
        button = pygame.Rect(width[i], height[i], button_width, button_height)
        buttons.append(button)

    modes = ['Classic', 'Chase', '1 VS 1', 'Quit']
    title_font = pygame.font.Font("freesansbold.ttf", 50)
    button_font = pygame.font.Font("freesansbold.ttf", 25)
    quit = False

    # play the background music on the start screen
    pygame.mixer.init()
    pygame.mixer.music.load("music/pacman.mp3")
    pygame.mixer.music.play(-1)

    while not quit:
        for event in pygame.event.get():
            # click the button with mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for j in range(0, len(buttons)):
                        if buttons[j].collidepoint(event.pos):
                            gamemode = j+1
                            quit = True
                            play = True
                            if gamemode == 4:
                                quit = True
                                play = False

            elif event.type == pygame.QUIT:
                quit = True
                play = False

        # load and display the background image on the start screen
        background = pygame.transform.scale(
            pygame.image.load("images/startscreen.jpg"), (1050, 600))
        rect = background.get_rect(center=(display_width/2, display_height/2))
        screen.blit(background, rect)

        # title text of the game
        txt_rend = title_font.render('CMPUT 274 Pacman', True, (255, 255, 255))
        txt_rect = txt_rend.get_rect(center=(display_width/2,
                                             display_height/5))
        screen.blit(txt_rend, txt_rect)
        for i in range(0, len(buttons)):
            # display the buttons on the start of the screen
            pygame.draw.rect(screen, (255, i*60, i*40), buttons[i])
            text = button_font.render(modes[i], True, (0, 0, 0))
            text_rect = text.get_rect(center=(buttons[i].left +
                                              (button_width/2), buttons[i].top
                                              + (button_height/2)))
            screen.blit(text, text_rect)

        pygame.display.update()

    # stop playing the music after the game starts
    pygame.mixer.music.stop()

    return(play)


def map_load():
    """
    Description: load the pacman map for a chosen mode
    Returns: random_colour(list): a list of length 3 that contains
             the RGB values of a colour(range from integer 0 to 255)
    """
    global pacman_map
    # Load the Classic mode map
    if gamemode == 1:
        map_file = open('pacmaps/pacmap_mode1.txt', 'r')
    # Load the Maze mode map, there are 3 maps for this mode which will
    # be randomly choosed.
    elif gamemode == 2:
        num = random.randint(0, 2)
        if num == 0:
            map_file = open('pacmaps/pacmap_mode2.1.txt', 'r')
        elif num == 1:
            map_file = open('pacmaps/pacmap_mode2.2.txt', 'r')
        elif num == 2:
            map_file = open('pacmaps/pacmap_mode2.3.txt', 'r')
    # Load the 1 VS 1 mode map
    else:
        map_file = open('pacmaps/pacmap_mode3.txt', 'r')
    pacman_map = map_file.read().splitlines()

    # Creates a nested list(2D list) where the outer lists represents the rows
    # and inner lists represents the columns
    for i in range(len(pacman_map)):
        pacman_map[i] = list(pacman_map[i])

    # Generates random colour for the wall, this is in the map_load function
    # instead of the map_draw function because map_draw will be called in a
    # while loop which will generate a random colour each time it runs.
    random_colour = []
    for i in range(0, 3):
        random_num = random.randint(0, 255)
        # a random colour will be selected for the background
        random_colour.append(random_num)

    return(random_colour)


def map_draw(random_colour):
    """
    Description: draw the pacman map to the display window
    Args: random_colour(list): a list of length 3 that contains
          the RGB values of a colour(range from integer 0 to 255)
    """
    global pacman_map
    # initialize necessary variables
    x = 0
    y = 0
    pacdot_colour = (0, 0, 255)

    # draw the map by looping through every element in the 2D list
    for line_list in pacman_map:
        for element in line_list:
            if element == 'X' or element == '#':
                # draws the walls to the screen
                pygame.draw.rect(screen, random_colour,
                                 (x, y, rect_width, rect_height), 2)

            # the maze mode have no pacdots
            if gamemode != 2:
                if element == '1':
                    # draws the pacdots to the screen
                    pygame.draw.circle(screen, pacdot_colour,
                                       (int(x+rect_width/2),
                                        int(y+rect_height/2)), 5, 0)

            x += rect_width
        x = 0
        y += rect_height


def display():
    """
    Description: display the text to the screen. There are two types of texts,
    game end message and score/time statistics.

    """

    global pacman, end

    # initialize font type and size
    stats_font = pygame.font.SysFont('roboto', 30)
    endmsg_font = pygame.font.SysFont('roboto', 70)
    white = (255, 255, 255)
    # set 3 modes for the game
    if gamemode == 1:
        # set the score text for the first mode
        text = stats_font.render("Score:"+str(pacman.score), True, white)
        screen.blit(text, (0, 0))

    elif gamemode == 2:
        # display the remaining time for the second mode
        text = stats_font.render("Remaining Time:"+str(counter), True, white)
        screen.blit(text, (0, 0))
    elif gamemode == 3:
        # display score and remaining time for the third mode
        time = stats_font.render("Remaining Time:"+str(counter), True, white)
        pac_score = stats_font.render("Pacman Score:"+str(pacman.score),
                                      True, white)
        py_score = stats_font.render("Pyman Score:"+str(pyman.score),
                                     True, white)
        screen.blit(time, (370, 450))
        screen.blit(pac_score, (0, 450))
        screen.blit(py_score, (800, 450))

        if counter <= 0 or end:
            # end game message for 1 VS 1 mode
            if pacman.score <= 0 and pyman.score <= 0:
                end_msg = endmsg_font.render("It's a draw!", True, white)
            elif pacman.score > pyman.score or pyman.score <= 0:
                end_msg = endmsg_font.render("Pacman Win!", True, white)
            elif pyman.score > pacman.score or pacman.score <= 0:
                end_msg = endmsg_font.render("Pyman Win!", True, white)
            else:
                end_msg = endmsg_font.render("It's a draw!", True, white)
            screen.blit(end_msg, (320, 180))

    if gamemode != 3:
        if pacman.score <= 0 or counter <= 0:
            # the game ends if score is less than 0 or no timeleft
            end_msg = endmsg_font.render("Game Over!", True, white)
            screen.blit(end_msg, (320, 180))
            end = True

    if won or (eaten[0] and eaten[1] and eaten[2] and eaten[3]):
        win_msg = endmsg_font.render("You Win!", True, white)
        screen.blit(win_msg, (320, 180))


def back_button():
    """
    Description: a back button that will appear on the bottom right hand
    corner of the screen that allows player to go back to the start screen.

    Returns: play(bool): return True if the back button is pressed, return
    false if the quit button is pressed.
    """
    global eaten, counter, won

    buttonR = pygame.Rect(950, 500, 100, 100)
    button_font = pygame.font.Font("freesansbold.ttf", 25)
    text_surf = button_font.render('Back', True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(1000, 550))
    loop = True
    while loop:
        for event in pygame.event.get():
            # check if the back button is pressed by the left mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttonR.collidepoint(event.pos):
                        # reset/reintialize some variables to play consecutive
                        # games
                        loop = False
                        play = True
                        eaten = [False, False, False, False]
                        counter = 50
                        won = False

            # check if the quit button on the top left hand corner is pressed
            elif event.type == pygame.QUIT:
                loop = False
                play = False

            pygame.draw.rect(screen, (0, 191, 255), buttonR)
            screen.blit(text_surf, text_rect)
            pygame.display.update()

    return (play)


def random_dots():
    """
        Description: For gamemode 3(1 VS 1 mode) only, it will randomly
        generate pacdots to the screen.
    """

    global pacman_map

    # generate two random numbers, one for the row coordinate and one for
    # the column coordinate
    row_num = random.randint(0, len(pacman_map))
    col_num = random.randint(0, len(pacman_map[row_num-1]))
    if pacman_map[row_num-1][col_num-1] == 'O':
        pacman_map[row_num-1][col_num-1] = '1'


def ghost_init():
    """
        Description: initialize all ghost objects for the chosen mode.
        Returns: ghost_list(list) : a list that contains 4 ghost objects.
    """

    ghost_list = []
    # ghost name information and start positions, the numbers on the variables
    # correspond to the mode.
    ghost_name_set13 = ["orange", "red", "blue", "pink"]
    ghost_name_set2 = ["cpp", "arduino", "python", "java"]
    start_pos13 = [[5, 28], [11, 28], [1, 12], [7, 5]]
    start_pos2 = [[1, 1], [1, 33], [15, 1], [15, 33]]
    for i in range(0, 4):
        if gamemode != 2:
            ghost = ghosts(start_pos13[i][0], start_pos13[i][1],
                           ghost_name_set13[i], pacman_map, "right")
            ghost_list.append(ghost)
        else:
            ghost = ghosts(start_pos2[i][0], start_pos2[i][1],
                           ghost_name_set2[i], pacman_map, "right")
            ghost_list.append(ghost)

    return(ghost_list)


def gm1_loop(ghost_list):
    """
    Description: a function that tracks all the game statistics for
    gamemode 1(Classic mode).
    Args: ghost_list(list): a list that contains 4 ghost objects.
    """

    global won
    checked = []
    count = 0
    # loop through the 2D list to check if all the pacdots are eaten by pacman
    for i in range(len(pacman.m)):
        for j in range(len(pacman.m[i])):
            if i in checked:
                continue
            # check if there are pacdots(i.e 1's) left on each row
            elif '1' not in pacman.m[i]:
                count += 1
                checked.append(i)
            if count == len(pacman.m):
                won = True

    for i in range(0, 4):
        # tracks if the pacman collides with the ghost
        pacman.dodge(ghost_list[i], ghost_list[i].name)
        # draw all ghosts objects to the screen
        ghost_list[i].draw(screen)


def gm2_loop(ghost_list):
    """
    Description: a function that tracks if each ghost have been "eaten" by
    Pacman.
    Args: ghost_list(list): a list that contains 4 ghost objects.
    """
    for i in range(0, 4):
        if not eaten[i]:
            eaten[i] = pacman.chase(ghost_list[i])
            # ghosts are not eaten will be showed on screen
            ghost_list[i].draw(screen)


def gm3_loop(ghost_list):
    """ Description: a function that tracks all the game statistics for
    gamemode 3(1 VS 1 mode).
    Args: ghost_list(list): a list that contains 4 ghost objects.
    """
    # the dots will appear on the screen randomly
    random_dots()
    pyman.draw(screen)
    for i in range(0, 4):
        ghost_list[i].draw(screen)
        # determine if the pacman/pyman collides with the ghost
        pacman.dodge(ghost_list[i], ghost_list[i].name)
        pyman.dodge(ghost_list[i], ghost_list[i].name)


def gameloop():
    """
    Description: the main loop that will run forever while the game is on.
    Returns: play(bool): return False if the quit button is pressed by the
    user, return True otherwise.
    """
    global pacman_map, pacman, pyman, won, counter, end
    # load the map and get the RGB values of the wall colour generated randomly
    wall_colour = map_load()

    # Create the pacman(and pyman, for mode 3) object(s).
    pacman = Pacman(9, 16, pacman_map, "right", "pacman")
    if gamemode == 3:
        pyman = Pacman(9, 18, pacman_map, "right", "pyman")

    # initialize the timer to tick every 1000ms(1s)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    end = False
    play = True

    # intialize the ghost objects
    ghost_list = ghost_init()

    while not won and not end:
        # control the pacman with 4 move keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.Left()
                elif event.key == pygame.K_RIGHT:
                    pacman.Right()
                elif event.key == pygame.K_UP:
                    pacman.Up()
                elif event.key == pygame.K_DOWN:
                    pacman.Down()
                pacman.eat_pacdot()

                if gamemode == 3:
                    # add another 4 keys for pyman in mode 3
                    if event.key == pygame.K_a:
                        pyman.Left()
                    elif event.key == pygame.K_d:
                        pyman.Right()
                    elif event.key == pygame.K_w:
                        pyman.Up()
                    elif event.key == pygame.K_s:
                        pyman.Down()
                    pyman.eat_pacdot()

            # tracks if the user pressed the quit button
            if event.type == pygame.QUIT:
                play = False
                end = True

            if gamemode != 1:
                # set time count down for mode 2 and 3
                if event.type == pygame.USEREVENT:
                    counter -= 1

        # determine the end conditions for the game(different end conditions
        # apply to each mode)
        if pacman.score <= 0 or counter <= 0 or \
           (eaten[0] and eaten[1] and eaten[2] and eaten[3]):
            screen.fill((0, 0, 0))
            end = True
        if gamemode == 3:
            if pyman.score <= 0:
                screen.fill((0, 0, 0))
                end = True

        screen.fill((0, 0, 0))
        # draw the map with the correspond random colour
        map_draw(wall_colour)

        # the loop part is different for each mode
        if gamemode == 1:
            gm1_loop(ghost_list)
        elif gamemode == 2:
            gm2_loop(ghost_list)
        elif gamemode == 3:
            gm3_loop(ghost_list)

        pacman.draw(screen)
        # set the 4 ghosts as different modes
        modes = [1, 2, 3, 2]

        for i in range(0, 4):
            if gamemode == 2:
                # all ghosts for mode 2 move randomly
                ghost_list[i].move(pacman, 2)
            else:
                # each ghost will follow their own algorithm based their
                # given mode defined in the mode list(this mode is different
                # from gamemode)
                ghost_list[i].move(pacman, modes[i])

        # calls the display function to display texts if certain
        # condition is satisfied
        display()

        # update the screen
        pygame.display.flip()

        # set the frame rate per second(fps)
        clock = pygame.time.Clock()
        clock.tick(66)

    return(play)


def main():
    play = True
    # There are three menus in the display screen, the start screen, in game
    # screen and the back button screen when game ends. Each menu the boolean
    # variable "play" tracks if the quit button is pressed by the player.
    # In the start screen it also tracks if the actual "Quit" button is pressed
    while play:
        setup()
        play = start_screen()
        if play:
            play = gameloop()
            if play:
                play = back_button()

    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
