import random
import pygame
import pygame.freetype

# game settings
fieldSize = 9
mines = 10
field = []
boxSize = 30

# Set the window size
screen_width = 600
screen_height = 600

# debug print minefield data
def tabledata(data):
    for row in field:
        rowpos = []
        for square in row:
            rowpos.append(square[data])
        print(rowpos)

def makeField():
    # create mine field
    minecounter = 0
    # starting pos of display
    ypos = (screen_height / 2) - ((boxSize + boxSize/6) * fieldSize)/2
    y = 0
    for i in range(fieldSize):
        row = []
        xpos = (screen_width / 2) - ((boxSize + boxSize/6) * fieldSize)/2
        x = 0
        for e in range(fieldSize):
            data = [] # rect, pos, mine, flag, clicked, surrounding mines
            # rect
            data.append(pygame.Rect(xpos, ypos, boxSize, boxSize))
            # pos
            data.append((x, y))
            # mine
            data.append(False)
            # flagged
            data.append(False)
            # clicked
            data.append(False)
            # surrounding mines
            data.append(0)
            row.append(data)
            xpos += boxSize + boxSize / 6
            x += 1
        field.append(row)
        ypos += boxSize + boxSize / 6
        y += 1
    # random generate mines in field
    while minecounter != mines:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        # add mines
        for row in field:
            for square in row:
                if square[1][0] == x and square[1][1] == y:
                    if square[2] == False:
                        square[2] = True
                        minecounter += 1
        
    # get number of mines around safe square
    for row in field:
        for square in row:
            # if selected square is a mine
            if square[2]:
                # get square pos
                xpos, ypos = square[1]
                surroundpos = []
                # get surrounding square pos
                surroundpos.append((xpos - 1, ypos - 1))
                surroundpos.append((xpos, ypos - 1))
                surroundpos.append((xpos + 1, ypos - 1))
                surroundpos.append((xpos - 1, ypos))
                surroundpos.append((xpos + 1, ypos))
                surroundpos.append((xpos - 1, ypos + 1))
                surroundpos.append((xpos, ypos + 1))
                surroundpos.append((xpos + 1, ypos + 1))
                # find pos
                for row in field:
                    for square in row:
                        # if it is a mine set mine to 9 since max mines surrounding is 8
                        if square[2]:
                            square[5] = 9
                        for pos in surroundpos:
                            if square[1] == pos:
                                if not square[2]:
                                    square[5] += 1

makeField()

# Initialize Pygame
pygame.init()

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper by Dex")
screen.fill(BLACK)

# set game info
clicked_squares = []
clicked_mine = False

# text
font_size = 24
font_color = BLUE
font = pygame.freetype.Font(None, font_size)

for row in field:
    for square in row:
        rect = square[0]
        square.append(pygame.draw.rect(screen, WHITE, rect))

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # get player clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Left mouse clicked
                for row in field:
                    for square in row:
                        if square[0].collidepoint(event.pos) and not square[3]:
                            # Square is clicked and not flagged
                            exist = False
                            square[4] = True  # Set the square as clicked
                            if square[2]:
                                # It's a mine
                                clicked_mine = True
                            else:
                                for clickedSquare in clicked_squares:
                                    if square[1] == clickedSquare[1]:  # Compare pos
                                        exist = True
                                # It's not a mine
                                if not exist:
                                    clicked_squares.append(square) 
            elif event.button == 3:  # flag box
                for row in field:
                    for square in row:
                        if square[0].collidepoint(event.pos):
                            square[3] = True
        # display buttons here

        # Update the screen
        pygame.display.update()

        if clicked_mine:
            print("Game Over!")
        elif len(clicked_squares) == (fieldSize * fieldSize) - mines:
            print("You Win!")

    # update game
    # note: rect, pos, mine, flag, clicked, surrounding mines
    for row in field:
        for square in row:
            if clicked_mine:  # display mine clicked
                if square[2]:
                    rect = square[0]
                    square.append(pygame.draw.rect(screen, RED, rect))
            for clickedSquare in clicked_squares:
                if square == clickedSquare:  # display the mines around box
                    rect = square[0]
                    square.append(pygame.draw.rect(screen, GREEN, rect))
                    text = str(square[5])
                    text_surface, _ = font.render(text, font_color)

                    text_rect = text_surface.get_rect()
                    text_rect.center = rect.center

                    screen.blit(text_surface, text_rect)
                if square[3]:  # flag box
                    rect = square[0]
                    square.append(pygame.draw.rect(screen, ORANGE, rect))

    pygame.display.update()

# Quit Pygame
pygame.quit()