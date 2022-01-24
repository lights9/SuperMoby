import os
from sys import exit
from os import path
import pickle

import pygame

pygame.init()  # to start game
clock = pygame.time.Clock()  # set maximum framerate
fps = 60  # framepersec

SCREENHEIGHT = 700
SCREENWIDTH = 700  # 640, 480

# define variables
tile_size = 50
game_over = 0
main_menu = True
level = 0
max_levels = 2

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.fill((100, 201, 207))  # 64C9CF
pygame.display.set_caption('Super Moby')

# load images
#background = pygame.image.load(os.path.join('backgrounds', 'probe.jpg'))
restart_img = pygame.image.load(os.path.join('assets', 'restart_btn.png'))
start_img = pygame.image.load('assets/start_btn.png')
exit_img = pygame.image.load('assets/exit_btn.png')


# function to reset level
def reset_level(level):
    player.reset(100, SCREENHEIGHT - 130)
    dino_group.empty()
    flag_group.empty()

    # load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            # [0] --> the index 0 --> left mouse button
            # checks if button is clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)
        return action


# dimensions for character
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

        # self.jumpCount = 7
        # self.left = False
        # self.right = False
        # self.walkCount = 0
        # self.standing = True;
        # self.hitbox = (self.x +20, self.y, 28, 60)

    def update(self, game_over):

        dy = 0
        dx = 0
        animation = 5
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.isJumping == False and self.in_air == False:
                self.vel = -15
                self.isJumping = True
            if key[pygame.K_SPACE] == False:
                self.isJumping = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.mirror = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.mirror = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.mirror == 1:
                    self.image = self.images_right[self.index]
                if self.mirror == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > animation:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.mirror == 1:
                    self.image = self.images_right[self.index]
                if self.mirror == -1:
                    self.image = self.images_left[self.index]

            self.vel += 1
            if self.vel > 15:
                self.vel = 10
            dy += self.vel

            # check for collision
            self.in_air = True

            for tile in world.tile_list:
                # x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel = 0
                    elif self.vel >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel = 0
                        self.in_air = False
            # check for collision with enemies
            if pygame.sprite.spritecollide(self, dino_group, False):
                game_over = -1

            # check for collision with flag
            if pygame.sprite.spritecollide(self, flag_group, False):
                game_over = 1

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

            # if self.rect.bottom > SCREENHEIGHT:
            #     self.rect.bottom = SCREENHEIGHT
            #     dx = 0

        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(0, 7):
            img_right = pygame.image.load(f'mobyCha/r{num}.png')
            img_left = pygame.image.load(f'mobyCha/l{num}.png')
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('mobyCha/dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.x = x  # 10
        self.y = y  # 370
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()  # 40
        self.height = self.image.get_height()  # 60
        self.vel = 0
        self.isJumping = False
        self.in_air = True
        self.mirror = 0


class World():
    def __init__(self, data):
        self.tile_list = []
        sand_img = pygame.image.load(os.path.join('objects2', '0.png'))
        shell_img = pygame.image.load(os.path.join('objects2', '1.png'))
        star_img = pygame.image.load(os.path.join('objects2', '2.png'))

        row_count = -1
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    img = pygame.transform.scale(sand_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # for collision
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 1:
                    img = pygame.transform.scale(shell_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # for collision
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(star_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # for collision
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    dino = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    # groups = .add
                    dino_group.add(dino)
                if tile == 6:
                    flag = Flag(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    flag_group.add(flag)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):  # want enemy class to be a child of the Sprite class (Sprite has some functions)
    def __init__(self, x, y):  # constructor
        pygame.sprite.Sprite.__init__(self)  # calling constructor from superclass
        self.image = pygame.image.load('enemy/front-e.png')
        # position enemy with rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        # if it is negative --> it will convert to an absolute value --> always positive
        if abs(self.move_counter) > 50:
            # if it is positive it becomes negative, if it is negative it becomes positive
            self.move_direction *= -1
            # when it goes to 51, it becomes -51
            self.move_counter *= -1


world_data = [
    [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 0],
    [1, -1, -1, -1, -1, -1, 2, 0, 1, 0, -1, -1, 0, 1],
    [1, 0, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
    [0, -1, 0, 0, 2, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    [0, 2, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, 0],
    [0, -1, -1, -1, -1, -1, -1, 2, 0, 1, 2, -1, -1, 0],
    [0, -1, -1, -1, -1, -1, -1, -1, 2, 0, -1, -1, -1, 2],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, 4, 5, -1, 1, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0],
    [1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 0],
    [0, -1, -1, -1, -1, 0, 1, -1, -1, -1, -1, -1, -1, 0],
    [0, -1, -1, -1, 0, 0, 1, -1, -1, -1, -1, -1, 3, 1],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
]

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('objects2/6.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(100, SCREENHEIGHT - 130)
dino_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()

# load in level data and create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# create buttons
restart_btn = Button(SCREENWIDTH // 2 - 50, SCREENHEIGHT // 2 + 100, restart_img)
start_button = Button(SCREENWIDTH // 2 - 350, SCREENHEIGHT // 2, start_img)
exit_button = Button(SCREENWIDTH // 2 + 150, SCREENHEIGHT // 2, exit_img)

# main loop
# moby = Player(40, 585, 40, 60)
# dino = Enemy(40, 585, 40, 40, 930)
# speed = 27 --> fps
run = True
while run:
    clock.tick(fps)  # set FBS to 27

    screen.blit(screen, (0, 0))
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            dino_group.update()

        # works because draw methode is in sprite class included
        dino_group.draw(screen)
        flag_group.draw(screen)

        game_over = player.update(game_over)

        # if player has died
        if game_over == -1:
            if restart_btn.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0

        # if player has completed the level
        if game_over == 1:
            # reset game and go to next level
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_btn.draw():
                    level = 1
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
exit()
