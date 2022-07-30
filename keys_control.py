from tank import *
from settings import *
from objects import *


def add_tank_by_key(user_input, random_x, random_y, t_name, random_color, volume):
    if user_input[pygame.K_q]:  # bind Q add tank
        sound_tank_add(volume/2)
        tanks.append(Tank(random_x, random_y, SCREEN, tank_speed, t_name, random_color, 0,
                          random.randint(0, 3), 0, all_volume))
        for tank in tanks:      # Check collision other tank
            rect_tank = tank.rect
            for other in tanks:
                rect_other = other.rect
                if rect_tank.colliderect(rect_other) and rect_other != rect_tank:
                    tanks.pop(tanks.index(other))
            for bomb in bombs:      # # Check collision bomb
                rect_bomb = bomb.rect
                if rect_bomb.colliderect(rect_tank):
                    tanks.pop(tanks.index(tank))
            for red_star in red_stars:      # # Check collision star
                rect_red_star = red_star.rect
                if rect_red_star.colliderect(rect_tank):
                    try:
                        tanks.pop(tanks.index(tank))
                    except ValueError:
                        pass
            for wall in objects:
                rect_w = wall.rect
                if rect_tank.colliderect(rect_w):
                    try:
                        tanks.pop(tanks.index(tank))
                    except ValueError:
                        pass


# -------- Bind R build wall ------
def key_build_wall(user_input, walls_max, width, height):
    for tank in tanks:
        # ----- Left side ----
        if user_input[pygame.K_r] and tanks.index(tank) == 0 and tank.side == tank.tank_sides[2] \
                and len(objects) < walls_max-6 and tank.rect.x < width - title_size - 20:
            x, y = tank.rect.topleft
            new_rect = pygame.Rect(x + title_size, y, title_size, title_size)
            fined = True
            for obj in objects:
                if new_rect.colliderect(obj.rect):
                    fined = False
            for t in tanks:
                if new_rect.colliderect(t.rect):
                    fined = False
            if fined:
                WallBrick(x + 100, y, block_brick)
        # ----- Right side -------
        elif user_input[pygame.K_r] and tanks.index(tank) == 0 and tank.side == tank.tank_sides[3]\
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
                WallBrick(x - 100, y, block_brick)
        # ----- Up side -------
        elif user_input[pygame.K_r] and tanks.index(tank) == 0 and tank.side == tank.tank_sides[0]\
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
                WallBrick(x, y + 100, block_brick)
        # ----- Down side -------
        elif user_input[pygame.K_r] and tanks.index(tank) == 0 and tank.side == tank.tank_sides[1]\
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
                WallBrick(x, y - 100, block_brick)


def keys_movie(user_input, current_time, volume):
    for tank in tanks:
        rect_tank = tank.rect
        old_tank_x, old_tank_y = tank.rect.x, tank.rect.y

        # -------- Tank Fire -------
        if user_input[pygame.K_e] and tanks.index(tank) == 0:
            tank.shot(current_time, volume/2)
        tank.second_shot(volume)

        if user_input[pygame.K_a] and tanks.index(tank) == 0:
            tank.m_down = tank.m_up = tank.m_right = False
            tank.go_left()
            tank.m_left = True
            tank.set_time_move(0)
        elif user_input[pygame.K_d] and tanks.index(tank) == 0:
            tank.m_down = tank.m_up = tank.m_left = False
            tank.go_right()
            tank.m_right = True
            tank.set_time_move(0)
        elif user_input[pygame.K_w] and tanks.index(tank) == 0:
            tank.m_down = tank.m_left = tank.m_right = False
            tank.go_up()
            tank.m_up = True
            tank.set_time_move(0)
        elif user_input[pygame.K_s] and tanks.index(tank) == 0:
            tank.m_left = tank.m_up = tank.m_right = False
            tank.go_down()
            tank.m_down = True
            tank.set_time_move(0)

        # -------- Tank collision wall -------
        for wall in objects:
            rect_wall = wall.rect
            if rect_tank.colliderect(rect_wall):
                tank.rect.x, tank.rect.y = old_tank_x, old_tank_y




