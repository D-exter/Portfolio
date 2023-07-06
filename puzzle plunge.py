import pygame
import json

def field(screen_width, screen_height):
    global playerxpos, playerypos, currentpressed, playerpos, grid, wallList, goalList, coinList, gamestart
    # get size for each box
    grid_size = len(grid), len(grid[0])
    field_size = screen_height - 150
    boxSize = field_size / max(grid_size)
    # get player pos
    xpos = (screen_width - screen_height + 150) // 2
    ypos = (screen_height - field_size) // 2
    if playerxpos == 0 and playerypos == 0:
        for row in grid:
            for square in row:
                if square == 1:
                    playerxpos = xpos
                    playerypos = ypos
                    xpos += boxSize
                else:
                    xpos += boxSize
            ypos += boxSize
            xpos = (screen_width - screen_height + 150) / 2
    # get box data
    xpos = (screen_width - screen_height + 150) // 2
    ypos = (screen_height - field_size) // 2
    gridRect = []
    for row in grid:
        gridRectRow = []
        for square in row:
            # set box data
            boxData = (square, pygame.Rect(xpos, ypos, boxSize, boxSize))
            xpos += boxSize
            gridRectRow.append(boxData)
        ypos += boxSize
        xpos = (screen_width - screen_height + 150) / 2
        gridRect.append(gridRectRow)
    # box color 
    playerRow = 0
    for row in gridRect:
        playercolumn = 0
        for boxdata in row:
            boxtype = boxdata[0]
            box = boxdata[1]
            if boxtype == 0:
                pygame.draw.rect(screen, WHITE, box)
            if boxtype == 1:
                pygame.draw.rect(screen, WHITE, box)
            if boxtype == 2:
                pygame.draw.rect(screen, BLUE, box)
                wallList.append((playerRow, playercolumn))
            if boxtype == 3:
                Goal = pygame.draw.rect(screen, RED, box)
                add = True
                # add goal to goal list
                for goal in goalList:
                    if goal[1] == Goal:
                        add = False
                if add:
                    goalList.append(((playerRow, playercolumn), Goal))
            if boxtype == 4:
                Coin = pygame.draw.rect(screen, YELLOW, box)
                add = True
                # add coin to coin list
                for coin in coinList:
                    if coin[1] == Coin:
                        add = False
                if add:
                    coinList.append(((playerRow, playercolumn), Coin))
            if boxtype == 5:
                pygame.draw.rect(screen, BLACK, box)
            # draw player
            if playerRow == playerpos[0] and playercolumn == playerpos[1]:
                player = pygame.draw.rect(screen, GREEN, box)
                # collect coin
                for coin in coinList:
                    if player.colliderect(coin[1]):
                        grid[playerRow][playercolumn] = 0
                        coinList.pop(coinList.index(coin))
                # reach goal
                for goal in goalList:
                    if player.colliderect(goal[1]):
                        if coinList == []:
                            print('end')

                            gamestart = False

            playercolumn += 1
        playerRow += 1
    
    # player input
    Keys = pygame.key.get_pressed()

    if Keys[pygame.K_w] and currentpressed == 'NONE':
        currentpressed = 'w'
    if Keys[pygame.K_a] and currentpressed == 'NONE':
        currentpressed = 'a'
    if Keys[pygame.K_s] and currentpressed == 'NONE':
        currentpressed = 's'
    if Keys[pygame.K_d] and currentpressed == 'NONE':
        currentpressed = 'd'
    
    # player movement
    if currentpressed != 'NONE':
        if currentpressed == 'w':
            move = True
            for wall in wallList:
                check = playerpos[0], playerpos[1]
                if check[0] == wall[0] and check[1] == wall[1]:
                    move = False
            if move:
                playerpos[0] -= 1
            else:
                playerpos[0] += 1
                currentpressed = 'NONE'
        
        if currentpressed == 'a':
            move = True
            for wall in wallList:
                check = playerpos[0], playerpos[1]
                if check[0] == wall[0] and check[1] == wall[1]:
                    move = False
            if move:
                playerpos[1] -= 1
            else:
                playerpos[1] += 1
                currentpressed = 'NONE'

        if currentpressed == 's':
            move = True
            for wall in wallList:
                check = playerpos[0], playerpos[1]
                if check[0] == wall[0] and check[1] == wall[1]:
                    move = False
            if move:
                playerpos[0] += 1
            else:
                playerpos[0] -= 1
                currentpressed = 'NONE'

        if currentpressed == 'd':
            move = True
            for wall in wallList:
                check = playerpos[0], playerpos[1]
                if check[0] == wall[0] and check[1] == wall[1]:
                    move = False
            if move:
                playerpos[1] += 1
            else:
                playerpos[1] -= 1
                currentpressed = 'NONE'

def start_game():
    global playerxpos, playerypos, currentpressed, playerpos, grid, wallList, goalList, coinList, Selected_level
    # set player pos
    playerxpos = 0
    playerypos = 0
    currentpressed = 'NONE'

    # info
    # 0 = bg    WHITE
    # 1 = player    GREEN
    # 2 = wall  BLUE
    # 3 = goal  RED
    # 4 = coin  YELLOW
    # 5 = black bg  BLACK
    
    # read level file
    with open('zgames/byMe/levels.json', 'r') as f:
        level = json.load(f)
    maxlevel = len(level)
    if maxlevel == Selected_level:
        Selected_level = 0    # set selected level
    grid = level[Selected_level]
    Selected_level += 1
    wallList = []
    goalList = []
    coinList = []

    # get player position
    playerRow = 0
    for row in grid:
        playercolumn = 0
        for box in row:
            if box == 1:
                playerpos = [playerRow, playercolumn]
            playercolumn += 1
        playerRow += 1

# set up game
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)

screen_width = 1000
screen_height = 600
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("puzzle plunge")

gamestart = False
editormode = False
Selected_level = 0



running = True
clock = pygame.time.Clock()
while running:
    if not gamestart and not editormode:

        screen.fill(BLACK)

        # main menu
        button_width = 200
        button_height = 50

        button1_x = (screen_width - button_width) // 2
        button1_y = (screen_height - button_height) // 2 - 50
        button = pygame.Rect(button1_x, button1_y, button_width, button_height)
        # change play button based on current level
        if Selected_level == 0:
            text = 'start'
        else:
            text = str(Selected_level + 1)
        # blit text and button
        button1 = pygame.draw.rect(screen, WHITE, button)
        font = pygame.font.Font(None, 40)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)
        
        button2_x = (screen_width - button_width) // 2
        button2_y = (screen_height - button_height) // 2 + 50
        button = pygame.Rect(button2_x, button2_y, button_width, button_height)
        # level editor button
        text = 'Editor'
        button2 = pygame.draw.rect(screen, WHITE, button)
        font = pygame.font.Font(None, 40)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)
        
        # get player clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    start_game()
                    gamestart = True
                if button2.collidepoint(pos):
                    editormode = True
        
        clock.tick(20)
        pygame.display.update()

    elif editormode:  # player click level editor mode button
        selected_box = None
        force_box = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check player clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if it is left click
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for row in gridRect:
                        for boxdata in row:
                            box = boxdata[1]
                            if box.collidepoint(mouse_pos):
                                selected_box = boxdata
                # check right click
                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    for row in gridRect:
                        for boxdata in row:
                            box = boxdata[1]
                            if box.collidepoint(mouse_pos):
                                force_box = boxdata
            # check if space pressed to save edited level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    with open('zgames/byMe/levels.json', 'r') as f:
                        levels = json.load(f)

                    levels.append(level)

                    with open('zgames/byMe/levels.json', 'w') as f:
                        json.dump(levels, f)
                    editormode = False
                        
        screen.fill(BLACK)
        # empty editor level for player to edit
        playerxpos = 0 
        playerypos = 0
        try:
            if level == []:
                level = [
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
                ]
        except:
            level = [
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
                ]
        # get player pos
        playerRow = 0
        for row in level:
            playercolumn = 0
            for box in row:
                if box == 1:
                    playerpos = [playerRow, playercolumn]
                playercolumn += 1
            playerRow += 1
        
        grid_size = len(level), len(level[0])
        field_size = screen_height - 150
        boxSize = field_size / max(grid_size)
        xpos = (screen_width - screen_height + 150) // 2
        ypos = (screen_height - field_size) // 2
        if playerxpos == 0 and playerypos == 0:
            for row in level:
                for square in row:
                    if square == 1:
                        playerxpos = xpos
                        playerypos = ypos
                        xpos += boxSize
                    else:
                        xpos += boxSize
                ypos += boxSize
                xpos = (screen_width - screen_height + 150) / 2
        xpos = (screen_width - screen_height + 150) // 2
        ypos = (screen_height - field_size) // 2
        gridRect = []
        for row in level:
            gridRectRow = []
            for square in row:
                # get boxData
                boxData = (square, pygame.Rect(xpos, ypos, boxSize, boxSize))
                xpos += boxSize
                gridRectRow.append(boxData)
            ypos += boxSize
            xpos = (screen_width - screen_height + 150) / 2
            gridRect.append(gridRectRow)
        # display box color
        playerRow = 0
        for row in gridRect:
            playercolumn = 0
            for boxdata in row:
                boxtype = boxdata[0]
                box = boxdata[1]
                if boxtype == 0:
                    square = pygame.draw.rect(screen, WHITE, box)
                if boxtype == 1:
                    square = pygame.draw.rect(screen, GREEN, box)
                if boxtype == 2:
                    square = pygame.draw.rect(screen, BLUE, box)
                if boxtype == 3:
                    square = pygame.draw.rect(screen, RED, box)
                if boxtype == 4:
                    square = pygame.draw.rect(screen, YELLOW, box)
                if boxtype == 5:
                    pygame.draw.rect(screen, BLACK, box)
                playercolumn += 1
            playerRow += 1
        playerRow = 0
        
        # check clicked box current type and change it
        for row in gridRect:
            playercolumn = 0
            for boxdata in row:
                boxtype = boxdata[0]
                box = boxdata[1]
                if boxdata == selected_box:
                    if boxtype == 0:
                        level[playerRow][playercolumn] = 1
                    if boxtype == 1:
                        level[playerRow][playercolumn] = 2
                    if boxtype == 2:
                        level[playerRow][playercolumn] = 3
                    if boxtype == 3:
                        level[playerRow][playercolumn] = 4
                    if boxtype == 4:
                        level[playerRow][playercolumn] = 5
                    if boxtype == 5:
                        level[playerRow][playercolumn] = 0
                    selected_box = None
                if boxdata == force_box:
                    level[playerRow][playercolumn] = 0
                playercolumn += 1
            playerRow += 1
        clock.tick(30)

        pygame.display.update()

    else:
        # game start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
            
        # Draw field
        field(screen_width, screen_height)
        
        clock.tick(30)

        pygame.display.update()

pygame.quit()
