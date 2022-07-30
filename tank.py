import os
import sys
import pygame
import random
from settings import *
from sounds import *
from settings import *


# ---------------- Class -----------------
class Tank:
    """ x, y, screen, tank_speed, player_name, player_name_color, count_kills, side, level, volume"""
    tank_sides = (tank_sand_up, tank_sand_down, tank_sand_left, tank_sand_right)
    MIN_X = MIN_Y = 0
    MAX_X = WIDTH
    MAX_Y = HEIGHT

    def __init__(self, x, y, screen, speed, name, p_color, count_kill, side,
                 level, volume, message=''):
        self.side = self.tank_sides[side]
        self.side_number = 0
        self.rect = self.side.get_rect()
        self.star = star
        self.star_rect = self.star.get_rect()
        self.star = pygame.transform.scale(self.star, (self.star.get_width() // 3,
                                                       self.star.get_height() // 3))
        self.screen = screen
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.bullets = []
        self.name = name
        self.msg = message
        self.p_color = p_color
        self.current_time = 0
        self.bullet_next_time = 0
        self.time_now = 0
        self.m_left = False
        self.m_right = False
        self.m_up = False
        self.m_down = False
        self.count_kill = count_kill
        self._time_move = 0
        self._time_msg = 0
        self.cooldown_msg = 30000
        self.level = level
        self.volume = volume

    # __________ For moving sound _________
    def get_m_moving(self):
        return (self.m_left, self.m_right, self.m_up, self.m_down)

    @classmethod
    def set_screen(cls, width, height):
        cls.MAX_X = width - 90
        cls.MAX_Y = height - 90

    @classmethod
    def validate_x_max(cls, arg):
        return arg <= cls.MAX_X

    @classmethod
    def validate_y_max(cls, arg):
        return arg <= cls.MAX_Y

    # ----- Inner class bullet -----
    class Bullet:
        """ Bullet_side """

        def __init__(self, side, volume):
            self.side = side
            self.side_bullet = side
            self.volume = volume
            self.rect_bullet = self.side_bullet.get_rect()
            tank_fire.set_volume(self.volume / 2)
            tank_fire.play()

    # -------- Tank functions --------

    def set_old_position(self, old_x, old_y):
        self.rect.x = old_x
        self.rect.y = old_y

    def get_bullet_rect(self):
        for bullet in self.bullets:
            return bullet.rect_bullet

    def bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[0]:
                bul.rect_bullet.x = self.rect.x + 38
                bul.rect_bullet.y = self.rect.y + 38

    def del_bullet(self):
        for bullet in self.bullets:
            self.bullets.pop(self.bullets.index(bullet))

    def shot(self, bullet_time_now, volume):
        self.bullet_next_time = bullet_time_now + 500
        if self.side == self.tank_sides[2] and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_left, volume))
            self.bullet_start_position()
        elif self.side == self.tank_sides[3] and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_right, volume))
            self.bullet_start_position()
        elif self.side == self.tank_sides[0] and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_up, volume))
            self.bullet_start_position()
        elif self.side == self.tank_sides[1] and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_down, volume))
            self.bullet_start_position()

    def second_shot(self, volume):
        pass

    def bullet_draw(self):
        for bul in self.bullets:
            if bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x -= 10
            elif bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x += 10
            elif bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.y -= 10
            elif bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.y += 10
            # ----- delete bullet ------
            self.screen.blit(bul.side_bullet, bul.rect_bullet)
            if bul.rect_bullet.x < 0 or bul.rect_bullet.x > self.MAX_X + 90 or bul.rect_bullet.y < 0 \
                    or bul.rect_bullet.y > self.MAX_Y + 90:
                self.bullets.pop(self.bullets.index(bul))

    # ----- Draw -----
    def draw(self):
        self.screen.blit(self.side, self.rect)  # Draw tank
        person_font = font_tf.render(f'{self.name}:  ', True, self.p_color)
        count_kill_font = font_kyiv.render(f': {self.count_kill}', True, azur)
        self.screen.blit(person_font, (self.rect.x, self.rect.y + 38))  # Draw name
        self.screen.blit(self.star, (self.rect.x + 30, self.rect.y + 10))  # Draw star
        self.screen.blit(count_kill_font, (self.rect.x + 55, self.rect.y + 15))
        time_msg = self._time_msg + self.cooldown_msg     # Show message by second
        if self.current_time < time_msg:
            msg_font = font_tf.render(f'{self.msg}', True, (255, 0, 255))
            self.screen.blit(msg_font, (self.rect.x + 18, self.rect.y + 55))  # Draw msg

    def set_msg(self, mess):
        self.msg = mess

    def set_time_msg(self, time):
        self._time_msg = time

    # ------- move by keys -------
    def go_up(self):
        self.side = self.tank_sides[0]
        self.side_number = 0
        if self.rect.y > 0:
            self.rect.y -= self.speed

    def go_down(self):
        self.side = self.tank_sides[1]
        self.side_number = 1
        if self.rect.y < self.MAX_Y:
            self.rect.y += self.speed

    def go_left(self):
        self.side = self.tank_sides[2]
        self.side_number = 2
        if self.rect.x > 0:
            self.rect.x -= self.speed

    def go_right(self):
        self.side = self.tank_sides[3]
        self.side_number = 3
        if self.rect.x < self.MAX_X:
            self.rect.x += self.speed

    # ------- move by Twitch -----
    def set_current_time(self, now):
        self.current_time = now

    def set_time_move(self, time_move):
        self._time_move = time_move

    def up(self):
        time_move = self.time_now + self._time_move * 100
        if self.rect.y > 0 and self.current_time < time_move and self.m_up:
            self.side = self.tank_sides[0]
            self.side_number = 0
            self.rect.y -= self.speed
        elif self.rect.y <= 0 or self.current_time > time_move:
            self.m_up = False
            self.time_now = 0

    def down(self):
        time_move = self.time_now + self._time_move * 100
        if self.validate_y_max(self.rect.y) and self.current_time < time_move and self.m_down:
            self.side = self.tank_sides[1]
            self.side_number = 1
            self.rect.y += self.speed
        elif self.rect.y >= self.MAX_Y or self.current_time > time_move:
            self.m_down = False
            self.time_now = 0

    def left(self):
        time_move = self.time_now + self._time_move * 100
        if self.rect.x > 0 and self.current_time < time_move and self.m_left:
            self.side = self.tank_sides[2]
            self.side_number = 2
            self.rect.x -= self.speed
        elif self.rect.x <= 0 or self.current_time > time_move:
            self.m_left = False
            self.time_now = 0

    def right(self):
        time_move = self.time_now + self._time_move * 100
        if self.validate_x_max(self.rect.x) and self.current_time < time_move and self.m_right:
            self.side = self.tank_sides[3]
            self.side_number = 3
            self.rect.x += self.speed
        elif self.rect.x >= self.MAX_X or self.current_time > time_move:
            self.m_right = False
            self.time_now = 0


# ---------- Tank BLUE fast speed ----------
class TankBlue(Tank):
    tank_sides = (tank_blue_up, tank_blue_down, tank_blue_left, tank_blue_right)

    @classmethod
    def set_screen(cls, width, height):
        cls.MAX_X = width - 84
        cls.MAX_Y = height - 92

    def shot(self, bullet_time_now, volume):
        self.bullet_next_time = bullet_time_now + 500
        if self.side == tank_blue_left and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_left, volume))
            self.bullet_start_position()
        elif self.side == tank_blue_right and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_right, volume))
            self.bullet_start_position()
        elif self.side == tank_blue_up and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_up, volume))
            self.bullet_start_position()
        elif self.side == tank_blue_down and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_down, volume))
            self.bullet_start_position()

    def bullet_draw(self):
        for bul in self.bullets:
            if bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x -= 15
            elif bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x += 15
            elif bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.y -= 15
            elif bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.y += 15
            # ----- delete bullet ------
            self.screen.blit(bul.side_bullet, bul.rect_bullet)
            if bul.rect_bullet.x < 0 or bul.rect_bullet.x > self.MAX_X + 90 or bul.rect_bullet.y < 0 \
                    or bul.rect_bullet.y > self.MAX_Y + 90:
                self.bullets.pop(self.bullets.index(bul))

    # ----- Draw -----
    def draw(self):
        self.screen.blit(self.side, self.rect)  # Draw tank
        person_font = font_tf.render(f'{self.name}:  ', True, self.p_color)
        count_kill_font = font_kyiv.render(f': {self.count_kill}', True, azur)
        self.screen.blit(person_font, (self.rect.x, self.rect.y + 38))  # Draw name
        self.screen.blit(self.star, (self.rect.x + 30, self.rect.y + 10))  # Draw star
        self.screen.blit(count_kill_font, (self.rect.x + 55, self.rect.y + 15))
        time_msg = self._time_msg + self.cooldown_msg  # Show message by second
        if self.current_time < time_msg:
            msg_font = font_tf.render(f'{self.msg}', True, yellow)
            self.screen.blit(msg_font, (self.rect.x + 18, self.rect.y + 55))  # Draw msg


# ------- Tank DARK fast bullet + speed ------
class TankDark(Tank):
    tank_sides = (tank_dark_up, tank_dark_down, tank_dark_left, tank_dark_right)

    @classmethod
    def set_screen(cls, width, height):
        cls.MAX_X = width - 96
        cls.MAX_Y = height - 96

    def bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[0]:
                bul.rect_bullet.x = self.rect.x + 42
                bul.rect_bullet.y = self.rect.y + 42

    def shot(self, bullet_time_now, volume):
        self.bullet_next_time = bullet_time_now + 500
        if self.side == tank_dark_left and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_left, volume))
            self.bullet_start_position()
        elif self.side == tank_dark_right and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_right, volume))
            self.bullet_start_position()
        elif self.side == tank_dark_up and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_up, volume))
            self.bullet_start_position()
        elif self.side == tank_dark_down and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_down, volume))
            self.bullet_start_position()

    # ----- Draw -----
    def draw(self):
        self.screen.blit(self.side, self.rect)  # Draw tank
        person_font = font_tf.render(f'{self.name}:  ', True, self.p_color)
        count_kill_font = font_kyiv.render(f': {self.count_kill}', True, azur)
        self.screen.blit(person_font, (self.rect.x, self.rect.y + 38))  # Draw name
        self.screen.blit(self.star, (self.rect.x + 35, self.rect.y + 10))  # Draw star
        self.screen.blit(count_kill_font, (self.rect.x + 60, self.rect.y + 15))
        time_msg = self._time_msg + self.cooldown_msg  # Show message by second
        if self.current_time < time_msg:
            msg_font = font_tf.render(f'{self.msg}', True, (255, 255, 255))
            self.screen.blit(msg_font, (self.rect.x + 18, self.rect.y + 65))  # Draw msg

    def bullet_draw(self):
        for bul in self.bullets:
            if bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x -= 20
            elif bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x += 20
            elif bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.y -= 20
            elif bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.y += 20
            # ----- delete bullet ------
            self.screen.blit(bul.side_bullet, bul.rect_bullet)
            if bul.rect_bullet.x < 0 or bul.rect_bullet.x > self.MAX_X + 90 or bul.rect_bullet.y < 0 or bul.rect_bullet.y > self.MAX_Y + 90:
                self.bullets.pop(self.bullets.index(bul))


# -------- Tank RED double shot -------
class TankRed(Tank):
    tank_sides = (tank_red_up, tank_red_down, tank_red_left, tank_red_right)

    @classmethod
    def set_screen(cls, width, height):
        cls.MAX_X = width - 96
        cls.MAX_Y = height - 104

    def bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[0]:
                bul.rect_bullet.x = self.rect.x + 44
                bul.rect_bullet.y = self.rect.y + 44

    def shot(self, bullet_time_now, volume):
        self.bullet_next_time = bullet_time_now + 200
        if self.side == tank_red_left and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_left, volume))
            self.bullet_start_position()
            self.second_shot(volume)
        elif self.side == tank_red_right and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_right, volume))
            self.bullet_start_position()
            self.second_shot(volume)
        elif self.side == tank_red_up and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_up, volume))
            self.bullet_start_position()
            self.second_shot(volume)
        elif self.side == tank_red_down and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_down, volume))
            self.bullet_start_position()

    def second_bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[-1]:
                bul.rect_bullet.x = self.rect.x + 44
                bul.rect_bullet.y = self.rect.y + 44

    def second_shot(self, volume):
        if self.current_time > self.bullet_next_time and self.bullet_next_time != 0:
            if self.side == tank_red_left and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_left, volume))
                self.second_bullet_start_position()
            elif self.side == tank_red_right and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_right, volume))
                self.second_bullet_start_position()
            elif self.side == tank_red_up and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_up, volume))
                self.second_bullet_start_position()
            elif self.side == tank_red_down and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_down, volume))
                self.second_bullet_start_position()
            self.bullet_next_time = 0

    def draw(self):
        self.screen.blit(self.side, self.rect)  # Draw tank
        person_font = font_tf.render(f'{self.name}:  ', True, self.p_color)
        count_kill_font = font_kyiv.render(f': {self.count_kill}', True, azur)
        self.screen.blit(person_font, (self.rect.x, self.rect.y + 38))  # Draw name
        self.screen.blit(self.star, (self.rect.x + 35, self.rect.y + 10))  # Draw star
        self.screen.blit(count_kill_font, (self.rect.x + 55, self.rect.y + 15))
        time_msg = self._time_msg + self.cooldown_msg  # Show message by second
        if self.current_time < time_msg:
            msg_font = font_tf.render(f'{self.msg}', True, (255, 255, 255))
            self.screen.blit(msg_font, (self.rect.x + 18, self.rect.y + 65))  # Draw msg

    def bullet_draw(self):
        for bul in self.bullets:
            if bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x -= 25
            elif bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x += 25
            elif bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.y -= 25
            elif bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.y += 25
            # ----- delete bullet ------
            self.screen.blit(bul.side_bullet, bul.rect_bullet)
            if bul.rect_bullet.x < 0 or bul.rect_bullet.x > self.MAX_X + 90 or bul.rect_bullet.y < 0 or bul.rect_bullet.y > self.MAX_Y + 90:
                self.bullets.pop(self.bullets.index(bul))


# ------ Tank BIG Cant crush if low level ------
class TankBigRed(Tank):
    tank_sides = (tank_big_red_up, tank_big_red_down, tank_big_red_left, tank_big_red_right)

    @classmethod
    def set_screen(cls, width, height):
        cls.MAX_X = width - 104
        cls.MAX_Y = height - 104

    def bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[0]:
                bul.rect_bullet.x = self.rect.x + 20
                bul.rect_bullet.y = self.rect.y + 20
        # sound_tank_fire(all_volume)

    def shot(self, bullet_time_now, volume):
        self.bullet_next_time = bullet_time_now + 10
        if self.side == tank_big_red_left and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_left, volume))
            self.bullet_start_position()
        elif self.side == tank_big_red_right and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_right, volume))
            self.bullet_start_position()
        elif self.side == tank_big_red_up and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_up, volume))
            self.bullet_start_position()
        elif self.side == tank_big_red_down and len(self.bullets) < 1:
            self.bullets.append(self.Bullet(bullet_dark_down, volume))
            self.bullet_start_position()

    def second_bullet_start_position(self):
        for bul in self.bullets:
            if bul == self.bullets[-1] and bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.x = self.rect.x + 80
                bul.rect_bullet.y = self.rect.y + 20
            elif bul == self.bullets[-1] and bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.x = self.rect.x + 80
                bul.rect_bullet.y = self.rect.y + 20
            elif bul == self.bullets[-1] and bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x = self.rect.x + 20
                bul.rect_bullet.y = self.rect.y + 80
            elif bul == self.bullets[-1] and bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x = self.rect.x + 20
                bul.rect_bullet.y = self.rect.y + 80
            # sound_tank_fire(all_volume)

    def bullet_draw(self):
        for bul in self.bullets:
            if bul.side_bullet == bullet_dark_left:
                bul.rect_bullet.x -= 30
            elif bul.side_bullet == bullet_dark_right:
                bul.rect_bullet.x += 30
            elif bul.side_bullet == bullet_dark_up:
                bul.rect_bullet.y -= 30
            elif bul.side_bullet == bullet_dark_down:
                bul.rect_bullet.y += 30
            # ----- delete bullet ------
            self.screen.blit(bul.side_bullet, bul.rect_bullet)
            if bul.rect_bullet.x < 0 or bul.rect_bullet.x > self.MAX_X + 90 or bul.rect_bullet.y < 0 or bul.rect_bullet.y > self.MAX_Y + 90:
                self.bullets.pop(self.bullets.index(bul))

    def second_shot(self, volume):
        if self.current_time > self.bullet_next_time and self.bullet_next_time != 0:
            if self.side == tank_big_red_left and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_left, volume))
                self.second_bullet_start_position()
            elif self.side == tank_big_red_right and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_right, volume))
                self.second_bullet_start_position()
            elif self.side == tank_big_red_up and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_up, volume))
                self.second_bullet_start_position()
            elif self.side == tank_big_red_down and len(self.bullets) < 2:
                self.bullets.append(self.Bullet(bullet_dark_down, volume))
                self.second_bullet_start_position()
            self.bullet_next_time = 0

    def draw(self):
        self.screen.blit(self.side, self.rect)  # Draw tank
        person_font = font_tf.render(f'{self.name}:  ', True, self.p_color)
        count_kill_font = font_kyiv.render(f': {self.count_kill}', True, azur)
        self.screen.blit(person_font, (self.rect.x, self.rect.y + 38))  # Draw name
        self.screen.blit(self.star, (self.rect.x + 40, self.rect.y + 20))  # Draw star
        self.screen.blit(count_kill_font, (self.rect.x + 55, self.rect.y + 15))
        time_msg = self._time_msg + self.cooldown_msg  # Show message by second
        if self.current_time < time_msg:
            msg_font = font_tf.render(f'{self.msg}', True, (255, 255, 255))
            self.screen.blit(msg_font, (self.rect.x + 18, self.rect.y + 65))  # Draw msg
