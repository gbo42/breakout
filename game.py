import pygame
from core import *

# game settings
wsize = 50
hsize = 30
padding = 4
wblocks = 10
hblocks = 5
running = True
WIDTH = wsize * wblocks + padding * (wblocks-1)
HEIGHT = 500

# game objects
ball = Ball(WIDTH/2, HEIGHT - 40 - 10, WHITE)

player = Player(WIDTH/2 - 50, HEIGHT - 40, 100, 10, RED)

walls = [Wall(-10, 0, 10, HEIGHT, GRAYER),
         Wall(WIDTH, 0, 10, HEIGHT, GRAYER),
         Wall(0, -10, WIDTH, 10, GRAYER)]

blocks = []
for i in range(10):
    for j in range(10):
        blocks.append(Block(i, j, (100, j*25, 100), wsize, hsize, padding))

# pygame setup
pygame.init()
pygame.display.set_caption("Collision")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while running:
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            keyDown(event.key, player, ball)
        if event.type == pygame.KEYUP:
            keyUp(event.key, player)

    # game logic
    wallsv = [w.rect for w in walls]
    player.move(wallsv)
    ball.hitPlayer(player)
    wallsv.append(player.rect)
    ball.move(wallsv, blocks)

    # render
    screen.fill(GRAY)
    ball.draw(screen)
    player.draw(screen)
    for w in walls:
        w.draw(screen)
    for block in blocks:
        block.draw(screen)
    pygame.display.flip()

pygame.quit()
