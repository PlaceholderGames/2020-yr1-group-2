import pygame, sys, random
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

gameDisplay = pygame.Surface((screenW, screenH))  # used as the surface for rendering, which is scaled
pauseDisplay = pygame.Surface((screenW, screenH))


key_left = 0

key_right = 0

key_space = 32

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

#Geting Player animation
#global animation_frames
#animation_frames = {}

#def load_animation(path,frame_duration): #[7,7]
#    global animation_frames
#    animation_name = path.split('/')[-1]
#    animation_frame_data = []
#    n = 0
#    for frame in frame_duration:
#        animation_frame_id = animation_name + '_' + str(n)
#        img_loc = path + '/' + animation_frame_id + '.png'
#        animation_image = pygame.image.load(img_loc).convert()
#        animation_image.set_colorkey((255,255,255))
#        animation_frames[animation_frame_id] = animation_image.copy()
#        for i in range(frame):
#            animation_frame_data.append(animation_frame_id)
#        n += 1
#    return animation_frame_data

#def change_action (action_var, frame, new_value):
#    if action_var != new_value:
#        action_var = new_value
#        frame = 0
#    return action_var,frame

#animation_database = {}

#animation_database['Walk'] = load_animation('Textures/Eli/Walk', [7,7])
#animation_database['Idle'] = load_animation('Textures/Eli/Idle', [7,7,40])

#player_action = 'idle'
#player_frame = 0
#player_flip = False

log = open("input_log.txt", "w")
optionsTxt = open("options.txt","r+")

game_map = load_map('Levels/map')

#player_image = pygame.image.load('Textures/Eli/Idle/Idle_0.png')
spider_1_image = pygame.image.load('Spider_1.png')
spider_2_image = pygame.image.load('spider_2.png')


rock_iamge = pygame.image.load('Textures/Level 1/Block 1.png')
TILE_SIZE = rock_iamge.get_width()
rock2_iamge = pygame.image.load('Textures/Level 1/Block 2.png')
damage_iamge = pygame.image.load('Textures/Level 1/block 3.png')
end_iamge = pygame.image.load('Textures/Level 1/flag.png')
silly_cat = pygame.image.load('Textures/Level 1/silly_cat.png')



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


def readKeys():
    optionsTxt.seek(0)
    keys = optionsTxt.readline()
    if keys == "0":
        return 0
    elif keys == "1":
        return 1


def setKeys(toggle):
    global key_left, key_right
    setK = readKeys()
    if toggle == False:
        if setK == 0:
            key_left = 97
            key_right = 100

        if setK == 1:
            key_left = 276
            key_right = 275

    elif toggle == True:
        optionsTxt.seek(0)
        if setK == 0:
            key_left = 276
            key_right = 275
            optionsTxt.write("1")
        elif setK == 1:
            key_left = 97
            key_right = 100
            optionsTxt.write("0")
        optionsTxt.flush()


def drawCursor():
    drawText(">", 30, screen, cursor_rect.x, cursor_rect.y)


def cursorUp(state,menu):
    if menu == 1:
        if state == "start":
            state = "exit"
            cursor_rect.midtop =(400,500)
        elif state == "exit":
            state = "credits"
            cursor_rect.midtop = (400, 400)
        elif state == "credits":
            state = "options"
            cursor_rect.midtop =(400,300)
        elif state == "options":
            state = "start"
            cursor_rect.midtop =(400, 200)

    elif menu == 2:
        if state == "toggle":
            state = "test3"
            cursor_rect.midtop = (400, 400)
        elif state == "test3":
            state = "test2"
            cursor_rect.midtop =(400,300)
        elif state == "test2":
            state = "toggle"
            cursor_rect.midtop =(400, 200)

    if menu == 3:
        if state == "resume":
            state = "exit"
            cursor_rect.midtop =(400,400)
        elif state == "exit":
            state = "options"
            cursor_rect.midtop =(400,300)
        elif state == "options":
            state = "resume"
            cursor_rect.midtop =(400, 200)

    drawCursor()
    return state


def cursorDown(state, menu):
    if menu == 1:
        if state == "start":
            state = "options"
            cursor_rect.midtop =(400,300)
        elif state == "options":
            state = "credits"
            cursor_rect.midtop =(400,400)
        elif state == "credits":
            state = "exit"
            cursor_rect.midtop =(400, 500)
        elif state == "exit":
            state = "start"
            cursor_rect.midtop =(400, 200)

    elif menu == 2:
        if state == "toggle":
            state = "test2"
            cursor_rect.midtop = (400, 300)
        elif state == "test2":
            state = "test3"
            cursor_rect.midtop =(400,400)
        elif state == "test3":
            state = "toggle"
            cursor_rect.midtop =(400, 200)

    if menu == 3:
        if state == "resume":
            state = "options"
            cursor_rect.midtop =(400,300)
        elif state == "options":
            state = "exit"
            cursor_rect.midtop =(400,400)
        elif state == "exit":
            state = "resume"
            cursor_rect.midtop =(400, 200)

    drawCursor()
    return state


def mainMenu():
    menu = 1
    state = "start"
    running = True

    while running:


        screen.fill((75, 75, 75), (0,0,screenW,screenH))
        drawText("main menu", 50, screen, screenW/2, 50)
        drawText("start game", 30, screen, screenW / 2, 200)
        drawText("options", 30, screen, screenW / 2, 300)
        drawText("credits", 30, screen, screenW / 2, 400)
        drawText("exit", 30, screen, screenW / 2, 500)
        drawCursor()



        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_UP:
                    state = cursorUp(state, menu)
                elif event.key == K_DOWN:
                    state = cursorDown(state, menu)

                elif event.key == K_RETURN:
                    if state == "start":
                        game()
                    elif state == "options":
                        options()
                    elif state == "credits":
                        credits()
                    elif state == "exit":
                        pygame.quit()
                        sys.exit()



        pygame.display.update()
        clock.tick(60)


def options():
    menu = 2
    state = "toggle"
    cursor_rect.midtop = (400, 200)
    running = True
    while running:

        screen.fill((75, 75, 75), (0, 0, screenW, screenH))
        drawText("options", 50, screen, screenW / 2, 50)
        if readKeys() == 0:
            drawText("keys toggle / A D", 30, screen, screenW / 2, 200)
        elif readKeys() == 1:
            drawText("keys toggle / < >", 30, screen, screenW / 2, 200)
        drawText("test2", 30, screen, screenW / 2, 300)
        drawText("test3", 30, screen, screenW / 2, 400)
        drawCursor()

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    state = cursorUp(state, menu)
                elif event.key == K_DOWN:
                    state = cursorDown(state, menu)

                elif event.key == K_RETURN:
                    if state == "toggle":
                        setKeys(True)
                    elif state == "test2":
                        pass
                    elif state == "test3":
                        pass

        pygame.display.update()
        clock.tick(60)


def credits():
    #menu ="credits"
    running = True
    while running:
        screen.fill((75, 75, 75), (0, 0, screenW, screenH))
        drawText("credits", 50, screen, screenW / 2, 50)
        drawText("Hannah Jones ", 30, screen, screenW / 2, 200)
        drawText("Nicole Brown", 30, screen, screenW / 2, 300)
        drawText("Szymond Dyndesz", 30, screen, screenW / 2, 400)
        drawText("Callum T K Jeffery", 30, screen, screenW / 2, 500)


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

    menu=3
    state = "resume"
    running = True
    pause = False
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
    player_image = pygame.image.load('Textures/Eli/Idle/Idle_0.png')
    player_rect = pygame.Rect(65, 685, 64, 128)
    spider1_rect = pygame.Rect(9791, 576, 470, 240)
    animtimer = 0
    animcounter = 0

    pausetitle = "paused"
    pauseDisplay.set_alpha(200)
    pauseDisplay.fill((50, 50, 50))

    print(key_right, key_left)

    while running:  # game loop
        if not pause:


            log = open("input_log.txt", "a")
            log.write("new frame\n")
            log.write("player Position{}\n".format(player_rect))
            gameDisplay.fill((50, 50, 50))  # clear screen by filling it with blue

            true_scroll[0] += (player_rect.x - true_scroll[0] - 152) /20
            true_scroll[1] += (player_rect.y - true_scroll[1] - 406) /20

            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            pygame.draw.rect(gameDisplay, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
            for background_object in background_objects:
                obj_rect = pygame.Rect(int(background_object[1][0] - scroll[0] * background_object[0]),
                                       int(background_object[1][1] - scroll[1] * background_object[0]), background_object[1][2],
                                       background_object[1][3])
                if background_object[0] == 0.5:
                    pygame.draw.rect(gameDisplay, (14, 222, 150), obj_rect)
                else:
                    pygame.draw.rect(gameDisplay, (9, 91, 85), obj_rect)

            endTiles = []
            damageTiles = []
            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        gameDisplay.blit(rock_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                        tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                    if tile == '2':
                        gameDisplay.blit(rock2_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                        tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                    if tile == '3':
                        gameDisplay.blit(damage_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                        damageTiles.append(pygame.Rect(x * 64, y * 64, 64, 64))
                    if tile == '4':
                        gameDisplay.blit(end_iamge, (x * 64 - scroll[0], y * 64 - scroll[1]))
                        endTiles.append(pygame.Rect(x * 64, y * 64, 64, 64))
                    if tile == '5':
                        gameDisplay.blit(silly_cat, (x * 64 - scroll[0], y * 64 - scroll[1]))
                        if random.random() <=0.5:
                            endTiles.append(pygame.Rect(x * 64, y * 64, 64, 64))
                        else:
                            damageTiles.append(pygame.Rect(x * 64, y * 64, 64, 64))

                    x += 1
                y += 1

            player_movement = [0, 0]
            if moving_right == True:
                player_movement[0] += 5
            if moving_left == True:
                player_movement[0] -= 5
            player_movement[1] += vertical_momentum

            #Running the animation
    #        if player_movement[0] > 0: #Moving Right
    #            player_action,player_frame = change_action(player_action,player_frame,'walk')
    #            player_flip = False
    #        if player_movement[0] == 0:
    #            player_action, player_frame = change_action(player_action, player_frame, 'idle')
    #        if player_movement[0] < 0: # Moving Left
    #            player_action,player_frame = change_action(player_action,player_frame,'walk')
    #            player_flip = True

            #if vertical_momentum >=0:
                #vertical_momentum += 0.8
            #else:
                #vertical_momentum += 0.2

            if vertical_momentum > 10:
                vertical_momentum = 10

            colidingDamageTiles = collision_test(player_rect,damageTiles)

            if len(colidingDamageTiles) > 0:
                pause = True
                pausetitle = "ded"

            colidingEndTiles = collision_test(player_rect,endTiles)

            if len(colidingEndTiles) > 0:
                pause = True
                pausetitle = "win"

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

            if collisions['top'] == True:
                vertical_momentum = 0

            #Implamanting Player animation
    #        player_frame += 1
    #        if player_frame >= len(animation_database[player_action]):
    #            player_frame = 0
    #        player_image_id = animation_database [player_action][player_frame]
    #        player_image = animation_frames[player_image_id]
    #        display.blit(pygame.transform.flip(player_image,player_flip,False, (player_rect.x - scroll[0], player_rect.y - scroll[1])))
            gameDisplay.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
            gameDisplay.blit(spider_1_image, (spider1_rect.x, player_rect.y))

            for event in pygame.event.get():  # event loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == key_right:
                        moving_right = True
                        log.write("key down: Right/d\n")

                    if event.key == key_left:
                        moving_left = True
                        log.write("key down: left/a\n")

                    if event.key == K_SPACE:
                        log.write("key down: space/a\n")
                        if air_timer < maxAirTime and inAir and canJump:
                            air_timer = 0
                        canJump = False

                    if event.key == K_ESCAPE:
                        pause = True


                if event.type == KEYUP:
                    if event.key == key_right:
                        moving_right = False
                        log.write("key up: Right/d\n")
                    if event.key == key_left:
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
            elif keys[key_left] or keys[key_right]:
                if inAir == False:
                    animtimer+= 1
                    if animtimer >=10:
                        if animcounter == 0:
                            player_image = pygame.image.load('Textures/Eli/Walk/walk_1.png')
                            animcounter = 1
                        elif animcounter == 1:
                            player_image = pygame.image.load('Textures/Eli/Idle/Idle_0.png')
                            animcounter = 0
                        animtimer = 0



            #log.write("in air:{}\n".format(inAir))
            #print("in air:{}".format(inAir))
            #log.write("player speed, X/Y: {} \n\n".format(player_movement))
            #print("player speed, X/Y: {} ".format(player_movement))
            #print("player Position{}".format(player_rect))
            #print(canJump)
           # print("air timer", air_timer)
           # print("jump timer",jumpTimer)
            #print("playerx" , player_rect.x)
            #print("playery", player_rect.y)

            screen.blit(pygame.transform.scale(gameDisplay, WINDOW_SIZE), (0, 0))
            pygame.display.update()

        else:
            scale = 1.0 / float(8.0)
            surf_size = gameDisplay.get_size()
            scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
            surf = pygame.transform.smoothscale(gameDisplay, scale_size)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE and pausetitle == "paused":
                        pause = False
                    if event.key == K_UP and pausetitle == "paused":
                        state = cursorUp(state, menu)
                    elif event.key == K_DOWN and pausetitle == "paused":
                        state = cursorDown(state, menu)

                    elif event.key == K_RETURN:
                        if state == "resume" :
                            pause = False
                        elif state == "options":
                            options()
                        elif state == "exit":
                            running = False

            screen.blit(pygame.transform.smoothscale(surf, WINDOW_SIZE), (0, 0))
            screen.blit(pygame.transform.scale(pauseDisplay, WINDOW_SIZE), (0, 0))


            drawText(pausetitle, 50, screen, screenW / 2, 50)
            if pausetitle == "paused":
                drawText("resume", 30, screen, screenW / 2, 200)
                drawText("options", 30, screen, screenW / 2, 300)
                drawText("exit", 30, screen, screenW / 2, 400)
            else:
                state = "exit"
                drawText("exit", 30, screen, screenW / 2, 200)

            drawCursor()

            pygame.display.update()

        clock.tick(60)


setKeys(False)
mainMenu()

