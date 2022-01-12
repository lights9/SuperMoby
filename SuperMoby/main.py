
import pygame

from sys import exit


pygame.init() #to start game


SCREENHEIGHT = 600
SCREENWIDTH = 800     #640, 480
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.fill((100, 201, 207))  #64C9CF
pygame.display.set_caption('Super Moby')

#dimensions for character
x = 50
y = 450
width = 40
height = 60
vel = 5


FramePerSec = pygame.time.Clock()  #set maximum framerate
FPS = 60   #framepersec
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
jumpCount = 10

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():  #gets list of all events that happen
        if event.type == pygame.QUIT:
            run = False

    #basics for moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < 800 - width - vel:
        x += vel

    if not(isJumping):
        if keys[pygame.K_UP] and y > vel:
           y -= vel
        if keys[pygame.K_DOWN] and y < 800 - height - vel:
           y += vel
        if keys[pygame.K_SPACE]:
           isJumping = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:  #negative number
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJumping = False
            jumpCount = 10


    #draw our character
    # draw all our elements
    # update everything
    screen.fill((100, 201, 207))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    pygame.display.update()
    FramePerSec.tick(FPS)  # tells pygame that this while loop should not run faster than 60times per second

pygame.quit()
exit()


    # #screen.blit(test_surface,(300,200))  #distance from left,top
    # for entity in all_sprites:
    #     screen.blit(entity.surf, entity.rect)








