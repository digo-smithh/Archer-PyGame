"""
Copyright (c) Eduardo Migueis and Rodrigo Smith 2020.
"""
import os
import sys
import pygame

pygame.init()

# font loading
font_path = '\\assets\\8bitOperatorPlus-Bold.ttf'
os.chdir(os.path.dirname(__file__))  # changes diroctory to load fonts
bit_small = pygame.font.Font(
    os.getcwd() + font_path, 20)
bit = pygame.font.Font(os.getcwd() + font_path, 60)
bit_extra_small = pygame.font.Font(
    os.getcwd() + font_path, 15)

# screen init and basic functions
scr_size = (width, height) = (1018, 549)
width = 1018
height = 549
FPS = 60

# assets loaded
screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Archer Game")
bg = pygame.image.load("assets/bg.png")
player = pygame.image.load("assets/archer1.png")
player_shoot = pygame.image.load("assets/archer2.png")
player = pygame.transform.scale(player, (300, 300))
player_shoot = pygame.transform.scale(player_shoot, (300, 300))
arrow = pygame.image.load("assets/arrow.png")
target = pygame.image.load("assets/target.png")
target = pygame.transform.scale(target, (170, 279))
target_lightning = pygame.image.load("assets/target_lightning.png")
target_lightning = pygame.transform.scale(target_lightning, (215, 690))

# glabal variables of logic
is_shooting = False
rect_y = 270
is_moving_down = True
shock_x = 1
points = 0

# message saved here to avoid repetition
err_msg = "Pygame display surface not rendering."


def gameplay():  # main method that controls how the gameplay goes
    playery = 0
    playerx = -80  # player x position

    gm_quit = False
    screen.blit(bg, (0, 0))  # empties the screen
    global is_shooting
    is_shooting = False
    while not gm_quit:  # main loop while user does not quit
        if pygame.display.get_surface() == None:  # verifies wether the display has been loaded or not
            print(err_msg)
            return True
        else:
            keys = pygame.key.get_pressed()  # checking pressed keys

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if playery > -50:
                    playery -= 3.5

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if playery < 300:
                    playery += 3.5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if user decides to quit, we stop the loop
                    gm_quit = True
                    return True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        screen.blit(bg, (0, 0))
                        screen.blit(player_shoot, (playerx, playery))
                        pygame.display.update()
                        is_shooting = True
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        shoot(playery, playerx + 30)

                    if event.key == pygame.K_ESCAPE:  # ESC key detected: back to intro screen
                        gm_quit = True
                        introScreen()
                        return True

            if not is_shooting:  # if the player is not shooting the arrows
                pygame.event.set_allowed(pygame.KEYDOWN)
                screen.blit(bg, (0, 0))
                screen.blit(player, (playerx, playery))

            global rect_change_y
            global rect_y
            global is_moving_down
            global shock_x

            shock_x = -shock_x
            if is_moving_down == True:
                rect_y += 2
                if rect_y > height/7:
                    rect_y += 1
                if rect_y > height/5:
                    rect_y += 1
                if rect_y > height/4:
                    rect_y += 2
                if rect_y > height/3:
                    rect_y += 2
            else:
                rect_y -= 2

            if rect_y > height - 275:
                is_moving_down = -is_moving_down
                rect_y = 275
            elif rect_y < 0:
                is_moving_down = -is_moving_down
                rect_y = 0

            if is_moving_down == True:
                screen.blit(target, (width - 174, rect_y))
            else:
                screen.blit(target_lightning, (width - 200 - shock_x, rect_y))

            global points
            pt = bit_small.render(str(points), True, (250, 250, 250))
            screen.blit(pt, (width - 75, 20))

            pygame.display.update()  # updates display and refreshes state of screen

        clock.tick(FPS)


def shoot(yStart, xStart):  # method that shoots the arrow and calculates where it landed
    arrowX = xStart + 70
    global is_moving_down
    global rect_y
    global shock_x
    global points
    crashed = False

    while arrowX < width:  # arrow animation
        screen.blit(bg, (0, 0))
        screen.blit(player_shoot, (xStart - 30, yStart))
        screen.blit(arrow, (arrowX, yStart + 90))
        pt = bit_small.render(str(points), True, (250, 250, 250))
        screen.blit(pt, (width - 75, 20))

        arrowX += 20
        shock_x = -shock_x

        if is_moving_down == True:
            rect_y += 2
            if rect_y > height/7:
                rect_y += 1
            if rect_y > height/5:
                rect_y += 1
            if rect_y > height/4:
                rect_y += 2
            if rect_y > height/3:
                rect_y += 2
        else:
            rect_y -= 2

        if rect_y > height - 275:
            is_moving_down = -is_moving_down
            rect_y = 275
        elif rect_y < 0:
            is_moving_down = -is_moving_down
            rect_y = 0

        if is_moving_down == True:
            screen.blit(target, (width - 174, rect_y))
        else:
            screen.blit(target_lightning, (width - 200 - shock_x, rect_y))

        pygame.display.update()

        # verifies if arrow has hit the target.
        if arrowX > width - 100 and yStart + 90 > rect_y - 40 and yStart + 90 < rect_y + 150 and crashed == False:
            # verifies where the arrow hit the target
            # rect_y is the center of the target image and yStart is the arrow height
            if yStart >= rect_y and yStart < rect_y + 40:
                points += 10
            elif yStart <= rect_y and yStart > rect_y - 30:
                points += 20
            elif yStart <= rect_y and yStart > rect_y - 50:
                points += 30
            elif yStart <= rect_y and yStart > rect_y - 60:
                points += 40
            elif yStart <= rect_y and yStart > rect_y - 70:
                points += 30
            elif yStart <= rect_y and yStart > rect_y - 100:
                points += 20
            elif yStart <= rect_y and yStart > rect_y - 170:
                points += 10
            crashed = True

        if arrowX > width - 100:
            global is_shooting
            is_shooting = False


def introScreen():  # loads the intro screen
    back_to_main = False
    while not back_to_main:
        global points
        points = 0
        screen.blit(bg, (0, 0))
        if pygame.display.get_surface() == None:
            print(err_msg)  # warns user something isn't able to load
            return True
        else:
            for event in pygame.event.get():  # detects keys to play or to leave
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    gameplay()
                    back_to_main = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    gameplay()
                    back_to_main = True
        if pygame.display.get_surface() != None:  # UI is shown
            title = bit.render("Archer Game", True, (250, 250, 250))
            screen.blit(title, (width/3 - 25, height/2 - 30))
            text = bit_small.render(
                "Press space or enter to star the game.", True, (250, 250, 250))
            screen.blit(text, (width/3 - 37, height/2 + 60))
            sub = bit_extra_small.render(
                "Points: yellow - 40, red - 30, black - 20, white - 10. Space to shoot.", True, (250, 250, 250))
            screen.blit(sub, (width - 585, height - 32))
            pygame.display.update()
        else:
            print(err_msg)

        clock.tick(FPS)


def main():  # main method calls intro screen loader
    introScreen()


main()
