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
ball = Ball(0, 0, WHITE)

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
    clock.tick(60)
    
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
    if ball.speed.x == 0 and ball.speed.y == 0:
        ball = Ball(player.x + 50, player.y - 10, WHITE)
    else:
        wallsv.append(player.rect)
        ball.hitPlayer(player)
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
