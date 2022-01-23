import os
import pygame
from sys import exit

pygame.init()  # to start game
clock = pygame.time.Clock()  # set maximum framerate
# FPS = 60   #framepersec

SCREENHEIGHT = 500
SCREENWIDTH = 1000  # 640, 480
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
#screen.fill((100, 201, 207))  # 64C9CF
pygame.display.set_caption('Super Moby')
background = pygame.image.load(os.path.join('backgrounds', 'bbbg.png'))
bgX = 0  # keep track of 2 different images at certain screen to never let screen turn blank
bgX2 = background.get_width()


# Zeynep Character Animation & Sprites AFTER CODE with pygame.display.set_caption
# images for walking left/right, staying still and background
# load player image
walkRight = [pygame.image.load(os.path.join('mobyCha', 'r1.png')), pygame.image.load(os.path.join('mobyCha', 'r2.png')),
             pygame.image.load(os.path.join('mobyCha', 'r3.png')), pygame.image.load(os.path.join('mobyCha', 'r4.png')),
             pygame.image.load(os.path.join('mobyCha', 'r5.png')), pygame.image.load(os.path.join('mobyCha', 'r6.png'))]
walkLeft = [pygame.image.load(os.path.join('mobyCha', 'l1.png')), pygame.image.load(os.path.join('mobyCha', 'l2.png')),
            pygame.image.load(os.path.join('mobyCha', 'l3.png')), pygame.image.load(os.path.join('mobyCha', 'l4.png')),
            pygame.image.load(os.path.join('mobyCha', 'l5.png')), pygame.image.load(os.path.join('mobyCha', 'l6.png'))]

charMoby = pygame.image.load(os.path.join('mobyCha', 'front.png'))


# dimensions for character
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x  # 10
        self.y = y  # 370
        self.width = width  # 40
        self.height = height  # 60
        self.vel = 5
        self.isJumping = False
        self.jumpCount = 7
        self.left = False
        self.right = False
        self.walkCount = 0

    def draw(self, screen):

        if self.walkCount + 1 >= 18:  # 18 because we have 9 sprites(png) for walking left/right, which each will be displayed in 3 frames
            self.walkCount = 0

        if moby.left:
            screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))  # //3 removes decimal
            self.walkCount += 1
            # scrollBackground(-5,0)

        elif moby.right:
            screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
            # scrollBackground(5, 0)
        else:
            screen.blit(charMoby, (self.x, self.y))


# Zeynep Character Animation & Sprites AFTER CODE with jumpCount = 10


# class enemy
class Enemy(object):
    walkRightEnemy = [pygame.image.load(os.path.join('enemy', 'r1-e.png')),
                      pygame.image.load(os.path.join('enemy', 'r2-e.png')),
                      pygame.image.load(os.path.join('enemy', 'r3-e.png')),
                      pygame.image.load(os.path.join('enemy', 'r4-e.png')),
                      pygame.image.load(os.path.join('enemy', 'r5-e.png')),
                      pygame.image.load(os.path.join('enemy', 'r6-e.png'))]
    walkLeftEnemy = [pygame.image.load(os.path.join('enemy', 'l1-e.png')),
                     pygame.image.load(os.path.join('enemy', 'l2-e.png')),
                     pygame.image.load(os.path.join('enemy', 'l3-e.png')),
                     pygame.image.load(os.path.join('enemy', 'l4-e.png')),
                     pygame.image.load(os.path.join('enemy', 'l5-e.png')),
                     pygame.image.load(os.path.join('enemy', 'l6-e.png'))]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 18:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRightEnemy[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeftEnemy[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0



def redraw_game_window():  # window
    screen.blit(background, (0, 0))
    screen.blit(background, (bgX, 0))
    screen.blit(background, (bgX2, 0))
    moby.draw(screen)
    dino.draw(screen)
    pygame.display.update()


# main loop
moby = Player(10, 370, 40, 60)
dino = Enemy(10, 370, 40, 40, 930)
speed = 27
run = True
while run:
    redraw_game_window()
    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < background.get_width() * -1:
        bgX = background.get_width()

    if bgX2 < background.get_width() * -1:
        bgX2 = background.get_width()

    for event in pygame.event.get():  # gets list of all events that happen
        if event.type == pygame.QUIT:
            run = False

    # basics for moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and moby.x > moby.vel:
        moby.x -= moby.vel
        moby.left = True
        moby.right = False
    elif keys[pygame.K_RIGHT] and moby.x < 1000 - moby.width - moby.vel:
        moby.x += moby.vel
        moby.right = True
        moby.left = False
    else:
        moby.right = False
        moby.left = False
        moby.walkCount = 0

    if not moby.isJumping:
        # if keys[pygame.K_UP] and y > vel:
        #    y -= vel
        # if keys[pygame.K_DOWN] and y < 800 - height - vel:
        #    y += vel
        if keys[pygame.K_SPACE]:
            moby.isJumping = True
            moby.right = False
            moby.left = False
            moby.walkCount = 0
    else:
        if moby.jumpCount >= -7:
            neg = 1
            if moby.jumpCount < 0:  # negative number
                neg = -1
            moby.y -= (moby.jumpCount ** 2) * 0.5 * neg
            moby.jumpCount -= 1
        else:
            moby.isJumping = False
            moby.jumpCount = 7

    pygame.display.update()
    clock.tick(speed)  # set FBS to 27

    # draw our character
    # draw all our elements
    # update everything
    # (made in the above lines, Zeynep)  FramePerSec.tick(FPS)
    # tells pygame that this while loop should not run faster than 60times per second

pygame.quit()
exit()

