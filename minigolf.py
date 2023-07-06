import pygame
import random

pygame.init()
pygame.font.init()


def walls(xpos, ypos, wallwidth, wallheight):
    return pygame.Rect(game_screen_xstart + xpos, game_screen_ystart + ypos, wallwidth, wallheight)


def hole(holexpos, holeypos):
    return holexpos, holeypos


def button(buttonxpos, buttonypos, buttonsize):
    return pygame.Rect(buttonxpos, buttonypos, buttonsize, buttonsize)


def draw_grass():
    grass_color = (144, 238, 144)
    for row in range(27):
        if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size + game_screen_xstart, row * cell_size + game_screen_ystart,
                                             cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 == 1:
                    grass_rect = pygame.Rect(col * cell_size + game_screen_xstart, row * cell_size + game_screen_ystart,
                                             cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)


pygame.display.set_caption('Mini Golf')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# setup game
width, height = 1000, 600
UIwidth, UIheigth = 300, 400
buttonsize = 60
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('Level Selector', False, WHITE)
text_surface_rect = text_surface.get_rect(center=(width // 2, height // 3))

mid_screen = (width // 2, height // 2)
screen = pygame.display.set_mode((width, height))
cell_size = 20
cell_number = 30
game_screen_xstart = 200
game_screen_ystart = 30

spawnx, spawny, spawnwidth, spawnheight = 0, 0, 0, 0
spawn = pygame.Rect(spawnx, spawny, spawnwidth, spawnheight)

running = True
game_active = False
win = False

player1_x, player1_y = 500, 300
player1_xspeed, player1_yspeed = 0, 0

gauge_start = (player1_x, player1_y)
gauge_end = (player1_x, player1_y)
maxspeed = 100
resistance = 4
ballsize = 10
holesize = ballsize * 1.2

shots = 0

holding = False
Start = 0
End = 0

wall_list = []
hole_list = []

while running:
    clock = pygame.time.Clock()
    clock.tick(60)

    pos = pygame.mouse.get_pos()
    # get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # when game is running
        if game_active:
            # ball movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if ball is clicked
                if player_1.collidepoint(pos):
                    Start = pos
                    holding = True
                # check if first shot allow player move ball in allowed area
                if shots == 0 and spawn.collidepoint(pos) and holding == 0:
                    player1_x = pos[0]
                    player1_y = pos[1]
            # calculate ball movement
            elif event.type == pygame.MOUSEBUTTONUP and holding:
                End = pos
                shots += 1
                xdiff = Start[0] - End[0]
                ydiff = Start[1] - End[1]
                if xdiff > maxspeed:
                    xdiff = maxspeed
                if xdiff < -maxspeed:
                    xdiff = -maxspeed
                if ydiff > maxspeed:
                    ydiff = maxspeed
                if ydiff < -maxspeed:
                    ydiff = -maxspeed
                player1_xspeed = xdiff / resistance
                player1_yspeed = ydiff / resistance
                gauge_end = (player1_x, player1_y)
                holding = False
            if holding:
                gauge_end = (Start[0] + (Start[0] - pos[0]), Start[1] + (Start[1] - pos[1]))

        else:
            # level list
            hole_list = []
            wall_list = []
            ballsize = 10
            # level selector and map generation
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(pos): # level 1
                    game_active = True
                    spawn = pygame.Rect(320, 430, 100, 30)
                    player1_x, player1_y = -100, -100
                    wall_list.append(walls(100, 100, 360, 20))
                    wall_list.append(walls(260, 240, 200, 20))
                    wall_list.append(walls(460, 100, 20, 160))
                    wall_list.append(walls(80, 100, 20, 360))
                    wall_list.append(walls(240, 260, 20, 200))
                    wall_list.append(walls(100, 440, 140, 20))
                    hole_list.append(hole(600, 210))
                if button2.collidepoint(pos):  # level 2
                    game_active = True
                    spawn = pygame.Rect(220, 310, 60, 60)
                    player1_x, player1_y = -100, -100
                    wall_list.append(walls(160, 200, 300, 20))
                    wall_list.append(walls(160, 400, 300, 20))
                    wall_list.append(walls(100, 270, 160, 80))
                    hole_list.append(hole(560, 340))
                if button3.collidepoint(pos):  # level 3
                    game_active = True
                    spawn = pygame.Rect(530, 250, 40, 160)
                    player1_x, player1_y = -100, -100
                    wall_list.append(walls(200, 200, 200, 10))
                    wall_list.append(walls(200, 400, 200, 10))
                    wall_list.append(walls(300, 210, 10, 190))
                    hole_list.append(hole(450, random.randint(300, 400)))
    if game_active:
        # player speed
        player1_x += player1_xspeed
        player1_y += player1_yspeed

        player1_xspeed *= 0.95
        player1_yspeed *= 0.95

        # background
        screen.fill(BLACK)
        background = pygame.draw.rect(screen, (50, 205, 50),
                                      pygame.Rect(game_screen_xstart, game_screen_ystart, (width - 400), height - 60))
        draw_grass()  # background

        # display shots
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f'Shots: {shots}', False, WHITE)
        text_surface_rect = text_surface.get_rect(center=(width // 1.15, height // 4))
        screen.blit(text_surface, text_surface_rect)

        # display game
        spawnbox = pygame.draw.rect(screen, ('#dd8a3c'), spawn)
        pygame.draw.line(screen, (0, 0, 0), gauge_start, gauge_end, 5)
        gauge_start = (player1_x, player1_y)
        gauge_end = (player1_x, player1_y)
        for walls in wall_list:  # draw walls
            pygame.draw.rect(screen, WHITE, walls)
            pygame.draw.rect(screen, BLACK, walls, 2)
        for holes in hole_list:  # draw hole
            hole = pygame.draw.circle(screen, BLACK, holes, holesize)
        player_1 = pygame.draw.circle(screen, WHITE, (int(player1_x), int(player1_y)), ballsize)
        pygame.draw.circle(screen, BLACK, (int(player1_x), int(player1_y)), ballsize, 2)
        pygame.display.update()

        # check game border collision
        if player_1.top < game_screen_ystart:
            player1_yspeed *= -1
        if player_1.bottom > height - game_screen_ystart:
            player1_yspeed *= -1
        if player_1.left < game_screen_xstart:
            player1_xspeed *= -1
        if player_1.right > width - game_screen_xstart:
            player1_xspeed *= -1

        # walls collision
        for walls in wall_list:
            if player_1.colliderect(walls):
                if player_1.left < walls.right < player_1.right:
                    player1_xspeed *= -1
                elif player_1.right > walls.left > player_1.left:
                    player1_xspeed *= -1
                else:
                    player1_yspeed *= -1

        # hole collision
        for holes in hole_list:
            if player_1.collidepoint(holes[0], holes[1]):
                player1_xspeed *= 0.90
                player1_yspeed *= 0.90
                if player1_xspeed < 0.005 and player1_yspeed < 0.005:
                    if player1_xspeed > -0.005 and player1_yspeed > -0.005:
                        win = True
        if win:  # animate ball falling in hole
            clock.tick(60)
            ballsize -= 0.2
            pygame.display.update()
            if ballsize < 0:
                running = False

    else:
        # background
        background = pygame.draw.rect(screen, (50, 205, 50),
                                      pygame.Rect(game_screen_xstart, game_screen_ystart, (width - 400), height - 60))
        draw_grass()
        pygame.draw.rect(screen, BLACK,
                         pygame.Rect(mid_screen[0] - (UIwidth // 2) - 5, mid_screen[1] - (UIheigth // 2) - 5,
                                     UIwidth + 10, UIheigth + 10))
        UI = pygame.draw.rect(screen, WHITE,
                              pygame.Rect(mid_screen[0] - (UIwidth // 2), mid_screen[1] - (UIheigth // 2), UIwidth,
                                          UIheigth))
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('Level Selector', False, BLACK)
        text_surface_rect = text_surface.get_rect(center=(width // 2, height // 3))
        screen.blit(text_surface, text_surface_rect)
        # level selector buttons
        button1 = pygame.draw.rect(screen, WHITE, button(363, 258, buttonsize))
        pygame.draw.rect(screen, BLACK, button(370, 250, buttonsize), 2)
        button2 = pygame.draw.rect(screen, WHITE, button(461, 258, buttonsize))
        pygame.draw.rect(screen, BLACK, button(470, 250, buttonsize), 2)
        button3 = pygame.draw.rect(screen, WHITE, button(561, 258, buttonsize))
        pygame.draw.rect(screen, BLACK, button(570, 250, buttonsize), 2)
        text_surface = my_font.render('1', False, BLACK)
        screen.blit(text_surface, button1.midtop)
        text_surface = my_font.render('2', False, BLACK)
        screen.blit(text_surface, button2.midtop)
        text_surface = my_font.render('3', False, BLACK)
        screen.blit(text_surface, button3.midtop)

        pygame.display.update()
