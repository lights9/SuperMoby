
import pygame
from sys import exit


pygame.init() #opposite to quit
screen = pygame.display.set_mode((800, 600))
screen.fill((100, 201, 207))  #64C9CF
pygame.display.set_caption('Super Moby')
clock = pygame.time.Clock()  #set maximum framerate

test_surface = pygame.Surface((100,200))
test_surface.fill((223, 113, 27))
#test_surface = pygame.image.load()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    screen.blit(test_surface,(200,100))  #distance from left,top

    #draw all our elements
    #update everything
    pygame.display.update()
    clock.tick(60)   #tells pygame that this while loop should not run faster than 60times per second







