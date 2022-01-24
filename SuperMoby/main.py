import os
from sys import exit

import pygame

pygame.init()  # to start game
clock = pygame.time.Clock()  # set maximum framerate
fps = 60  # framepersec

SCREENHEIGHT = 700
SCREENWIDTH = 700  # 640, 480
tile_size = 50
game_over = 0
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
# screen.fill((100, 201, 207))  # 64C9CF
pygame.display.set_caption('Super Moby')
background = pygame.image.load(os.path.join('backgrounds', 'probe.jpg'))
restart_img = pygame.image.load(os.path.join('assets', 'restart_btn.png'))


# bgX = 0  # keep track of 2 different images at certain screen to never let screen turn blank
# bgX2 = background.get_width()


# Zeynep Character Animation & Sprites AFTER CODE with pygame.display.set_caption
# images for walking left/right, staying still and background
# load player image
# walkRight = [pygame.image.load(os.path.join('mobyCha', 'r1.png')), pygame.image.load(os.path.join('mobyCha', 'r2.png')),
#              pygame.image.load(os.path.join('mobyCha', 'r3.png')), pygame.image.load(os.path.join('mobyCha', 'r4.png')),
#              pygame.image.load(os.path.join('mobyCha', 'r5.png')), pygame.image.load(os.path.join('mobyCha', 'r6.png'))]
# walkLeft = [pygame.image.load(os.path.join('mobyCha', 'l1.png')), pygame.image.load(os.path.join('mobyCha', 'l2.png')),
#             pygame.image.load(os.path.join('mobyCha', 'l3.png')), pygame.image.load(os.path.join('mobyCha', 'l4.png')),
#             pygame.image.load(os.path.join('mobyCha', 'l5.png')), pygame.image.load(os.path.join('mobyCha', 'l6.png'))]
#
# charMoby = pygame.image.load(os.path.join('mobyCha', 'front.png'))

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

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -=5

            # if self.rect.bottom > SCREENHEIGHT:
            #     self.rect.bottom = SCREENHEIGHT
            #     dx = 0

        screen.blit(self.image, self.rect)
        return game_over

        # def draw(self, screen):
        #
        #     if self.walkCount + 1 >= 18:  # 18 because we have 9 sprites(png) for walking left/right, which each will be displayed in 3 frames
        #         self.walkCount = 0
        #
        #     if self.left:
        #         screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))  # //3 removes decimal
        #         self.walkCount += 1
        #         # scrollBackground(-5,0)
        #
        #     elif self.right:
        #         screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
        #         self.walkCount += 1
        #         # scrollBackground(5, 0)
        #     else:
        #         screen.blit(charMoby, (self.x, self.y),)
        #         #pygame.draw.rect(screen, (255, 0, 0), (self.x+10, self.y+5, self.width, self.height), 2)

        # for tile in world.tile_list:
        #     #y collison
        #     if tile[1].colliderect(self.rect.x, self.rect.y + dy)

        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    # Zeynep Character Animation & Sprites AFTER CODE with jumpCount = 10

    # class enemy
    # class Enemy(object):
    #     walkRightEnemy = [pygame.image.load(os.path.join('enemy', 'r1-e.png')),
    #                       pygame.image.load(os.path.join('enemy', 'r2-e.png')),
    #                       pygame.image.load(os.path.join('enemy', 'r3-e.png')),
    #                       pygame.image.load(os.path.join('enemy', 'r4-e.png')),
    #                       pygame.image.load(os.path.join('enemy', 'r5-e.png')),
    #                       pygame.image.load(os.path.join('enemy', 'r6-e.png'))]
    #     walkLeftEnemy = [pygame.image.load(os.path.join('enemy', 'l1-e.png')),
    #                      pygame.image.load(os.path.join('enemy', 'l2-e.png')),
    #                      pygame.image.load(os.path.join('enemy', 'l3-e.png')),
    #                      pygame.image.load(os.path.join('enemy', 'l4-e.png')),
    #                      pygame.image.load(os.path.join('enemy', 'l5-e.png')),
    #                      pygame.image.load(os.path.join('enemy', 'l6-e.png'))]
    #
    #     def __init__(self, x, y, width, height, end):
    #         self.x = x
    #         self.y = y
    #         self.width = width
    #         self.height = height
    #         self.end = end
    #         self.path = [self.x, self.end]
    #         self.walkCount = 0
    #         self.vel = 3
    #
    #     def draw(self, win):
    #         self.move()
    #         if self.walkCount + 1 >= 18:
    #             self.walkCount = 0
    #         if self.vel > 0:
    #             win.blit(self.walkRightEnemy[self.walkCount //3], (self.x, self.y))
    #             self.walkCount += 1
    #         else:
    #             win.blit(self.walkLeftEnemy[self.walkCount //3], (self.x, self.y))
    #             self.walkCount += 1
    #
    #     def move(self):
    #
    #         if self.vel > 0:
    #             if self.x + self.vel < self.path[1]:
    #                 self.x += self.vel
    # #                self.rect.x += self.vel
    #             else:
    #                 self.vel = self.vel * -1
    #                 self.walkCount = 0
    #         else:
    #             if self.x - self.vel > self.path[0]:
    #                 self.x += self.vel
    # #                self.rect.x += self.vel
    #             else:
    #                 self.vel = self.vel * -1
    #                 self.walkCount = 0

    # def redraw_game_window():  # window
    #     screen.blit(background, (0, 0))
    #     screen.blit(background, (bgX, 0))
    #     screen.blit(background, (bgX2, 0))
    #     moby.draw(screen)
    #     dino.draw(screen)
    #     pygame.display.update()

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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


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
    [1, 0, -1, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
    [0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
    [0, 2, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, 0],
    [0, -1, -1, -1, -1, -1, -1, 2, 0, 1, -1, -1, -1, 0],
    [0, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 2],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, 4, 5, -1, 1, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0],
    [1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 0],
    [0, -1, -1, -1, -1, 0, 1, -1, -1, -1, -1, -1, -1, 0],
    [0, -1, -1, -1, 0, 0, 1, -1, -1, -1, -1, -1, 3, 1],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
]

player = Player(100, SCREENHEIGHT - 130)
dino_group = pygame.sprite.Group()
world = World(world_data)

# create buttons
restart_btn = Button(SCREENWIDTH // 2 - 50, SCREENHEIGHT // 2 + 100, restart_img)

# main loop
# moby = Player(40, 585, 40, 60)
# dino = Enemy(40, 585, 40, 40, 930)
# speed = 27 --> fps
run = True
while run:
    clock.tick(fps)  # set FBS to 27
    # redraw_game_window()
    # bgX -= 1.4
    # bgX2 -= 1.4
    # if bgX < background.get_width() * -1:
    #     bgX = background.get_width()
    #
    # if bgX2 < background.get_width() * -1:
    #     bgX2 = background.get_width()
    #
    # for event in pygame.event.get():  # gets list of all events that happen
    #     if event.type == pygame.QUIT:
    #         run = False

    # basics for moving
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT] and moby.x > moby.vel:
    #     dx -= moby.vel
    #     moby.x -= moby.vel
    #     moby.left = True
    #     moby.right = False
    # elif keys[pygame.K_RIGHT] and moby.x < 1000 - moby.width - moby.vel:
    #     dx += moby.vel
    #     moby.x += moby.vel
    #     moby.right = True
    #     moby.left = False
    # else:
    #     moby.right = False
    #     moby.left = False
    #     moby.walkCount = 0
    #
    # if not moby.isJumping:
    #     # if keys[pygame.K_UP] and y > vel:
    #     #    y -= vel
    #     # if keys[pygame.K_DOWN] and y < 800 - height - vel:
    #     #    y += vel
    #     if keys[pygame.K_SPACE]:
    #         moby.isJumping = True
    #         moby.right = False
    #         moby.left = False
    #         moby.walkCount = 0
    # else:
    #     if moby.jumpCount >= -7:
    #         neg = 1
    #         if moby.jumpCount < 0:  # negative number
    #             neg = -1
    #         moby.y -= (moby.jumpCount ** 2) * 0.5 * neg
    #         moby.jumpCount -= 1
    #     else:
    #         moby.isJumping = False
    #         moby.jumpCount = 7

    screen.blit(background, (0, 0))
    world.draw()

    if game_over == 0:
        dino_group.update()

    # works because draw methode is in sprite class included
    dino_group.draw(screen)

    game_over = player.update(game_over)

    # if player has died
    if game_over == -1:
        if restart_btn.draw():
            player.reset(100, SCREENHEIGHT - 130)
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

    # draw our character
    # draw all our elements
    # update everything
    # (made in the above lines, Zeynep)  FramePerSec.tick(FPS)
    # tells pygame that this while loop should not run faster than 60times per second

pygame.quit()
exit()
