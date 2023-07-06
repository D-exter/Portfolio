import pygame

# initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up the window display
width = 800
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong on ice")

# circle size
circley = width // 2
circlex = height // 2
circle_radius = 13

# circle velocity
circleyvel = 4
circlexvel = 4
rectangle = (26, 100)
square_surface = pygame.Surface(rectangle)

# players
player1x = 100
player1y = height // 2 - 50
player2x = 700
player2y = height // 2 - 50
player1vel = 0
player2vel = 0
square_color = WHITE

# player scores
player1score = 0
player2score = 0

clock = pygame.time.Clock()

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # circle movements
    circlex += circlexvel
    circley += circleyvel

    # circle hit ceiling
    if circley < 0:
        circley = -circley
        circleyvel *= -1

    # circle hit floor
    if circley > height - circle_radius:
        circley = 2 * (height - circle_radius) - circley
        circleyvel *= -1

    # circle hit right side of the screen
    if circlex < 0:
        circlex = width//2
        player2score += 1

    # circle hit left side of the screen
    if circlex > width:
        circlex = width//2
        player1score += 1

    # player 1 movements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1y > 0:
        player1vel -= 0.2
    if keys[pygame.K_s] and (player1y + rectangle[1]) < height:
        player1vel += 0.2
    # player2 movement
    if keys[pygame.K_UP] and player2y > 0:
        player2vel -= 0.2
    if keys[pygame.K_DOWN] and (player2y + rectangle[1]) < height:
        player2vel += 0.2

    # check if player1 out of screen
    if player1y < 0:
        player1vel = 0
        player1y = 0
    if (player1y + rectangle[1]) > height:
        player1vel = 0
        player1y = height - rectangle[1]

    # check if player2 out of screen
    if player2y < 0:
        player2vel = 0
        player2y = 0
    if (player2y + rectangle[1]) > height:
        player2vel = 0
        player2y = height - rectangle[1]

    # player velocity
    player1y += player1vel
    player2y += player2vel

    screen.fill(BLACK)

    # draw players
    square_rect1 = pygame.Rect(player1x, player1y, rectangle[0], rectangle[1])
    player1 = pygame.draw.rect(screen, square_color, square_rect1)
    square_rect2 = pygame.Rect(player2x, player2y, rectangle[0], rectangle[1])
    player2 = pygame.draw.rect(screen, square_color, square_rect2)

    # draw circle
    circle = pygame.draw.circle(screen, WHITE, (circlex, circley), circle_radius)  # Draw the circle

    # check if circle hit player1
    if circle.colliderect(player1):
        circlex = 135
        circlexvel = -circlexvel
        # check if player velocity not 0
        if player1vel != 0:
            # give ball a new direction
            circleyvel = 0
            circleyvel += player1vel

    # check if circle hit player2
    if circle.colliderect(player2):
        circlex = 690
        circlexvel = -circlexvel
        # check if player velocity not 0
        if player2vel != 0:
            # give ball a new direction
            circleyvel = 0
            circleyvel += player2vel

    # score
    font = pygame.font.Font(None, 36)
    score = str(player1score) + '  ' + str(player2score)
    text = font.render(score, True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (width//2, height//2)
    screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
