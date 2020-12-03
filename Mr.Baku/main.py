import pygame, sys
from os import system, name

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()  # initiates pygame

#default_font = pygame.font.SysFont(None, 20)
default_font = pygame.font.get_default_font()

pygame.display.set_caption("Mr.Baku")
icon = pygame.image.load('baku icon.png')
pygame.display.set_icon(icon)

screenW, screenH = 1280, 720

WINDOW_SIZE = (screenW, screenH)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface((screenW, screenH))  # used as the surface for rendering, which is scaled







def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map





log = open("input_log.txt", "w")


game_map = load_map('Levels/map')

player_image = pygame.image.load('Textures/Eli/RedEli.png')

rock_iamge = pygame.image.load('Textures/Level 1/Block 1.png')
TILE_SIZE = rock_iamge.get_width()
rock2_iamge = pygame.image.load('Textures/Level 1/Block 2.png')



cursor_rect = pygame.Rect(0, 0, 30, 30)
cursor_rect.midtop =(400,200)


background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                      [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += int(movement[1]+0.5) #round to closest integer
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def drawText(text, size, surface, x, y):
    font = pygame.font.Font(default_font, size)
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def drawCursor():
    drawText(">", 30, screen, cursor_rect.x, cursor_rect.y)

def cursorUp(state): ################## ONLY WORKS FOR MAIN MENU, I WILL IMPLEMENT FOR OTHER MENUS AS WELL
    if state == "start":
        state = "credits"
        cursor_rect.midtop =(400,400)
    elif state == "credits":
        state = "options"
        cursor_rect.midtop =(400,300)
    elif state == "options":
        state = "start"
        cursor_rect.midtop =(400, 200)
    drawCursor()
    return state

def cursorDown(state): ################## ONLY WORKS FOR MAIN MENU, I WILL IMPLEMENT FOR OTHER MENUS AS WELL
    if state == "start":
        state = "options"
        cursor_rect.midtop =(400,300)
    elif state == "options":
        state = "credits"
        cursor_rect.midtop =(400,400)
    elif state == "credits":
        state = "start"
        cursor_rect.midtop =(400, 200)
    drawCursor()
    return state

def mainMenu():
    state = "start"
    running = True
    while running:

        screen.fill((75, 75, 75), (0,0,screenW,screenH))
        drawText("main menu", 50, screen, screenW/2, 50)
        drawText("start game", 30, screen, screenW / 2, 200)
        drawText("options", 30, screen, screenW / 2, 300)
        drawText("credits", 30, screen, screenW / 2, 400)
        drawCursor()



        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_UP:
                    state = cursorUp(state)
                elif event.key == K_DOWN:
                    state = cursorDown(state)

                elif event.key == K_RETURN:
                    if state == "start":
                        game()
                    elif state == "options":
                        options()
                    elif state == "credits":
                        credits()



        pygame.display.update()
        clock.tick(60)


def options():
    running = True
    while running:

        screen.fill((75, 75, 75), (0, 0, screenW, screenH))
        drawText("options", 50, screen, screenW / 2, 50)

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


def credits():
    running = True
    while running:
        screen.fill((75, 75, 75), (0, 0, screenW, screenH))
        drawText("credits", 50, screen, screenW / 2, 50)

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

def game():

    running = True
    moving_right = False
    moving_left = False
    inAir = False
    canJump = False

    vertical_momentum = 0
    air_timer = 0
    jumpTimer = 0
    maxAirTime = 20  # use this for checking air timer
    jumpHeight = 10  # adjust this to make player jump higher or lower)

    true_scroll = [0, 0]

    player_rect = pygame.Rect(10, 640, 64, 128)


    while running:  # game loop

        log = open("input_log.txt", "a")
        log.write("new frame\n")
        log.write("player Position{}\n".format(player_rect))
        display.fill((50, 50, 50))  # clear screen by filling it with blue

        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) /20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 406) /20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(int(background_object[1][0] - scroll[0] * background_object[0]),
                                   int(background_object[1][1] - scroll[1] * background_object[0]), background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display, (14, 222, 150), obj_rect)
            else:
                pygame.draw.rect(display, (9, 91, 85), obj_rect)

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(rock_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                if tile == '2':
                    display.blit(rock2_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                x += 1
            y += 1

        player_movement = [0, 0]
        if moving_right == True:
            player_movement[0] += 5
        if moving_left == True:
            player_movement[0] -= 5
        player_movement[1] += vertical_momentum

        #if vertical_momentum >=0:
            #vertical_momentum += 0.8
        #else:
            #vertical_momentum += 0.2

        if vertical_momentum > 10:
            vertical_momentum = 10

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom'] == True:
            air_timer = 0
            jumpTimer = 0
            vertical_momentum = 0.8 #reset to falling gravity so player is constantly colliding

            inAir = False
            canJump = True
        else:
            if vertical_momentum >=1:
                vertical_momentum += 0.8
            else:
                vertical_momentum += 0.2
            air_timer += 1
            inAir = True

        display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                    log.write("key down: Right/d\n")

                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                    log.write("key down: left/a\n")

                if event.key == K_SPACE:
                    log.write("key down: space/a\n")
                    if air_timer < maxAirTime and inAir and canJump:
                        air_timer = 0
                    canJump = False

                if event.key == K_ESCAPE:
                    running = False


            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                    log.write("key up: Right/d\n")
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                    log.write("key up: left/a\n")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            log.write("key press: Space\n")
            if air_timer < maxAirTime and jumpTimer < jumpHeight:
                if vertical_momentum <-10:
                    vertical_momentum = -10
                else:
                    vertical_momentum -= 2
            jumpTimer += 1

        log.write("in air:{}\n".format(inAir))
        #print("in air:{}".format(inAir))
        log.write("player speed, X/Y: {} \n\n".format(player_movement))
        #print("player speed, X/Y: {} ".format(player_movement))
        #print("player Position{}".format(player_rect))
        print(canJump)
        print("air timer", air_timer)
        print("jump timer",jumpTimer)


        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)

mainMenu()
