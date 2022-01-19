import os
import pygame
from sys import exit


pygame.init() #to start game

SCREENHEIGHT = 500
SCREENWIDTH = 1000     #640, 480
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.fill((100, 201, 207))  #64C9CF
pygame.display.set_caption('Super Moby')

#Zeynep Character Animation & Sprites AFTER CODE with pygame.display.set_caption
#images for walking left/right, staying still and background
walkRight = [pygame.image.load(os.path.join('mobyCha','r1.png')),pygame.image.load(os.path.join('mobyCha','r2.png')), pygame.image.load(os.path.join('mobyCha','r3.png')), pygame.image.load(os.path.join('mobyCha','r4.png')), pygame.image.load(os.path.join('mobyCha','r5.png')), pygame.image.load(os.path.join('mobyCha','r6.png')), pygame.image.load(os.path.join('mobyCha','r7.png')), pygame.image.load(os.path.join('mobyCha','r8.png')), pygame.image.load(os.path.join('mobyCha','r9.png'))]
walkLeft = [pygame.image.load(os.path.join('mobyCha','l1.png')),pygame.image.load(os.path.join('mobyCha','l2.png')), pygame.image.load(os.path.join('mobyCha','l3.png')), pygame.image.load(os.path.join('mobyCha','l4.png')), pygame.image.load(os.path.join('mobyCha','l5.png')), pygame.image.load(os.path.join('mobyCha','l6.png')), pygame.image.load(os.path.join('mobyCha','l7.png')), pygame.image.load(os.path.join('mobyCha','l8.png')), pygame.image.load(os.path.join('mobyCha','l9.png'))]
bg = pygame.image.load(os.path.join('backgrounds','bbbg.png'))
char = pygame.image.load(os.path.join('mobyCha','front.png'))

#dimensions for character
x = 10
y = 170
width = 40
height = 60
vel = 5


FramePerSec = pygame.time.Clock()  #set maximum framerate
#FPS = 60   #framepersec
#test_surface = pygame.Surface((100,200))
#test_surface.fill((223, 113, 27))
#test_surface = pygame.image.load()

#
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((50, 50))
#         self.image.fill((128, 255, 40))
#         # self.rect = self.image.get_rect()
#         self.rect = self.image.get_rect(center=(10, 420))
#     # self.rect.center = (WIDTH / 2, HEIGHT / 2)
#
#
# P1 = Player()
# all_sprites = pygame.sprite.Group()
# all_sprites.add(P1)

isJumping = False
jumpCount = 7

#Zeynep Character Animation & Sprites AFTER CODE with jumpCount = 10
left = False
right = False
walkCount = 0

def redrawGameWindow(): #window
    global walkCount
    screen.blit(bg, (0,0))
    pygame.display.update()

    if walkCount + 1 >= 27: #27 because we have 9 sprites(png) for walking left/right, which each will be displayed in 3 frames
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount//3], (x,y)) # //3 removes decimal
        walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        screen.blit(char, (x,y))

    pygame.display.update()

#main loop
run = True
while run:
    FramePerSec.tick(27) # set FBS to 27

    for event in pygame.event.get():  #gets list of all events that happen
        if event.type == pygame.QUIT:
            run = False

    #basics for moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 700 - width - vel:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not(isJumping):
        # if keys[pygame.K_UP] and y > vel:
        #    y -= vel
        # if keys[pygame.K_DOWN] and y < 800 - height - vel:
        #    y += vel
        if keys[pygame.K_SPACE]:
            isJumping = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -7:
            neg = 1
            if jumpCount < 0:  #negative number
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJumping = False
            jumpCount = 7

    redrawGameWindow()


    #draw our character
    # draw all our elements
    # update everything
    #(made in the above lines, Zeynep)  FramePerSec.tick(FPS)  # tells pygame that this while loop should not run faster than 60times per second

pygame.quit()
exit()


    # #screen.blit(test_surface,(300,200))  #distance from left,top
    # for entity in all_sprites:
    #     screen.blit(entity.surf, entity.rect)








