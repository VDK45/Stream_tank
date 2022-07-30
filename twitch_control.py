import random
from tank import *
from settings import *
from objects import *


def add_tank_by_twitch_command(random_x, random_y, twitch_name, twitch_command, random_color, volume):
    if twitch_command == "!tank":
        rect_image = pygame.Rect(random_x, random_y, 100, 100)  # tank size 100/100
        add_tank = True
        for tank in tanks:
            rect_tank = tank.rect
            if tank.name == twitch_name:
                add_tank = False
            if rect_tank.colliderect(rect_image):  # Check collision other tank
                add_tank = False
        for bomb in bombs:  # Check collision bomb
            rect_bomb = bomb.rect
            if rect_bomb.colliderect(rect_image):
                add_tank = False
        for red_star in red_stars:  # Check collision star
            rect_red_star = red_star.rect
            if rect_red_star.colliderect(rect_image):
                add_tank = False
        for wall in objects:    # Check collision walls
            rect_w = wall.rect
            if rect_w.colliderect(rect_image):
                add_tank = False
        if add_tank:
            sound_tank_add(volume / 2)
            tanks.append(Tank(random_x, random_y, SCREEN, tank_speed,
                              twitch_name, random_color, 0, random.randint(0, 3), 0, all_volume))


def twitch_command_build(twitch_command, twitch_name, walls_max, width, height):
    for tank in tanks:
        # --------- build wall ---------
        # ----- Left side ----
        if twitch_command == "!build" and tank.name == twitch_name and tank.side == tank.tank_sides[2] \
                and len(objects) < walls_max-6 and tank.rect.x < width - title_size - 20:
            x, y = tank.rect.topleft
            new_rect = pygame.Rect(x + title_size, y, title_size, title_size)
            fined = True
            for obj in objects:
                if new_rect.colliderect(obj.rect):  # check collision other wall
                    fined = False
            for t in tanks:
                if new_rect.colliderect(t.rect):  # check collision other tank
                    fined = False
            if fined:
                WallBrick(x + title_size, y, block_brick)
        # ----- Right side -------
        elif twitch_command == "!build" and tank.name == twitch_name and tank.side == tank.tank_sides[3] \
                and len(objects) < walls_max-6 and tank.rect.x > 20:
            x, y = tank.rect.topleft
            new_rect = pygame.Rect(x - title_size, y, title_size, title_size)
            fined = True
            for obj in objects:
                if new_rect.colliderect(obj.rect):
                    fined = False
            for t in tanks:
                if new_rect.colliderect(t.rect):
                    fined = False
            if fined:
                WallBrick(x - title_size, y, block_brick)
        # ----- Up side -------
        elif twitch_command == "!build" and tank.name == twitch_name and tank.side == tank.tank_sides[0] \
                and len(objects) < walls_max-6 and tank.rect.y < height - title_size - 20:
            x, y = tank.rect.topleft
            new_rect = pygame.Rect(x, y + title_size, title_size, title_size)
            fined = True
            for obj in objects:
                if new_rect.colliderect(obj.rect):
                    fined = False
            for t in tanks:
                if new_rect.colliderect(t.rect):
                    fined = False
            if fined:
                WallBrick(x, y + title_size, block_brick)
        # ----- Down side -------
        elif twitch_command == "!build" and tank.name == twitch_name and tank.side == tank.tank_sides[1] \
                and len(objects) < walls_max-6 and tank.rect.y > 20:
            x, y = tank.rect.topleft
            new_rect = pygame.Rect(x, y - title_size, title_size, title_size)
            fined = True
            for obj in objects:
                if new_rect.colliderect(obj.rect):
                    fined = False
            for t in tanks:
                if new_rect.colliderect(t.rect):
                    fined = False
            if fined:
                WallBrick(x, y - title_size, block_brick)


def twitch_command_movie(twitch_command, twitch_name, time_move, current_time, volume):
    for tank in tanks:
        if twitch_command == "!left" and tank.name == twitch_name:
            tank.m_down = tank.m_up = tank.m_right = False
            tank.m_left = True
            tank.time_now = current_time
            tank.set_time_move(time_move)
        elif twitch_command == "!right" and tank.name == twitch_name:
            tank.m_down = tank.m_up = tank.m_left = False
            tank.m_right = True
            tank.time_now = current_time
            tank.set_time_move(time_move)
        elif twitch_command == "!up" and tank.name == twitch_name:
            tank.m_down = tank.m_left = tank.m_right = False
            tank.m_up = True
            tank.time_now = current_time
            tank.set_time_move(time_move)
        elif twitch_command == "!down" and tank.name == twitch_name:
            tank.m_left = tank.m_up = tank.m_right = False
            tank.m_down = True
            tank.time_now = current_time
            tank.set_time_move(time_move)

        # ---- shots ----
        if twitch_command == "!fire" and tank.name == twitch_name \
                or twitch_command == "!shot" and tank.name == twitch_name:
            tank.shot(current_time, volume/2)


def tank_movie_by_commands(current_time, WIDTH, HEIGHT):
    for tank in tanks:
        rect_tank = tank.rect
        old_tank_x, old_tank_y = tank.rect.x, tank.rect.y
        tank.set_current_time(current_time)
        tank.bullet_draw()
        tank.draw()
        tank.set_screen(WIDTH, HEIGHT)
        if tank.m_left:
            tank.left()
        elif tank.m_right:
            tank.right()
        elif tank.m_up:
            tank.up()
        elif tank.m_down:
            tank.down()
        for wall in objects:
            rect_wall = wall.rect
            if rect_tank.colliderect(rect_wall):
                tank.rect.x, tank.rect.y = old_tank_x, old_tank_y
