import pygame
import math

# colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GRAY = (51, 51, 51)
GRAYER = (200, 200, 200)

# helpers
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ball
class Ball:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x - 5, y - 5, 10, 10)
        self.x = x - 5
        self.y = y - 5
        self.color = color
        self.speed = Vector(0, 0)
        
    def start(self):
        self.speed = Vector(0, -1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    # collide with player and change speed
    def hitPlayer(self, player):
        tempx = self.x
        tempy = self.y
        self.x += self.speed.x + 5
        self.y += self.speed.y + 5
        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.colliderect(player.rect):
            tx = self.x - (player.x+50)
            ty = 50
            tm = math.sqrt(tx*tx + ty*ty)
            self.speed.x = tx/tm
            if self.speed.y < 0:
                self.speed.y = ty/tm
            else:
                self.speed.y = -ty/tm
        elif self.y > player.y + 50:
            self.speed.x = 0
            self.speed.y = 0

        self.x = tempx
        self.y = tempy
        self.rect.x = self.x
        self.rect.y = self.y


    # move and collide with walls
    def move(self, clist, blocks):
        tempx = self.x
        tempy = self.y
        self.x += self.speed.x
        self.y += self.speed.y

        self.rect.x = self.x
        block = self.rect.collidelist(clist)
        if block != -1:
            if self.speed.x < 0:
                self.rect.left = clist[block].right
            else:
                self.rect.right = clist[block].left
            self.speed.x = -self.speed.x
            self.x = self.rect.x
        self.rect.y = self.y
        block = self.rect.collidelist(clist)
        if block != -1:
            if self.speed.y < 0:
                self.rect.top = clist[block].bottom
            else:
                self.rect.bottom = clist[block].top
            self.speed.y = -self.speed.y
            self.y = self.rect.y

        for b in blocks:
            if self.hitBlock(b):
                blocks.remove(b)
                continue

    def hitBlock(self, block):
        hit = False
        tempx = self.rect.x
        tempy = self.rect.y


        self.rect.x = self.x + self.speed.x
        if self.rect.colliderect(block.rect):
            hit = True
            self.speed.x = -self.speed.x
        self.rect.x = tempx

        self.rect.y = self.y + self.speed.y
        if self.rect.colliderect(block.rect):
            hit = True
            self.speed.y = -self.speed.y
        self.rect.y = tempy

        return hit

# wall
class Wall:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# player
class Player:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.color = color
        self.speed = Vector(0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def changeSpeed(self, x, y):
        self.speed.x += x
        self.speed.y += y

    def move(self, clist):
        tempx = self.x
        self.x += self.speed.x

        self.rect.x = self.x
        block = self.rect.collidelist(clist)
        if block != -1:
            if self.speed.x < 0:
                self.rect.left = clist[block].right
            else:
                self.rect.right = clist[block].left
            self.x = self.rect.x

# block
class Block:
    def __init__(self, x, y, color, w, h, p):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect((x * (w + p), y * (h + p), w, h))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# handlers for key events
def keyDown(key, player, ball):
    if key == pygame.K_LEFT:
        player.changeSpeed(-1, 0)
    if key == pygame.K_RIGHT:
        player.changeSpeed(1, 0)
    if key == pygame.K_SPACE and ball.speed.x == 0 and ball.speed.y == 0:
        ball.start()

def keyUp(key, player):
    if key == pygame.K_LEFT:
        player.changeSpeed(1, 0)
    if key == pygame.K_RIGHT:
        player.changeSpeed(-1, 0)
