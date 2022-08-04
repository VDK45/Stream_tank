import pygame
import sys
import os
import json
import pyperclip
import getpass
import tkinter as tk
from tkinter import filedialog
from random import randint
from moviepy.editor import VideoFileClip

root = tk.Tk()
root.withdraw()


# ------ For convert to exe --------
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ----------------- Game stating ---------------------
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=8, buffer=1024, devicename=None)
intro = resource_path("assets/video_intro.mp4")
intro = VideoFileClip(intro)
# intro.preview()
video_tips = resource_path("assets/tips.mp4")
video_tips = VideoFileClip(video_tips)
video_tips_tr  = resource_path("assets/tips_transparent .mp4")
video_tips_transparent = VideoFileClip(video_tips_tr)

# ----------------- Window parameters ---------------
pygame.display.set_caption("Tank Twitch play")  # название окна
icon_win = resource_path('images/tanks/tank_big_red_up.png')
pygame.display.set_icon(pygame.image.load(icon_win))
bg_res = resource_path('assets/Background.png')
background_menu = pygame.image.load(bg_res)
RUN = True
FPS = 30

# ------------- Main menu -------------
rec_button_play = resource_path("assets/Play Rect.png")
bg_image_menu = resource_path("assets/Background.png")
font_menu_button = resource_path("assets/font.ttf")
rect_button_option = resource_path("assets/Options Rect.png")
button_quit = resource_path("assets/Quit Rect.png")
button_quit_rect = pygame.image.load(button_quit)
info_rect_res = resource_path("assets/info_rect.png")
info_rect = pygame.image.load(info_rect_res)

button_rect_res = resource_path("assets/button_rect.png")
button_rect = pygame.image.load(button_rect_res)
back_rect_res = resource_path("assets/back_rect.png")
back_rect = pygame.image.load(back_rect_res)
option_rect_res = resource_path("assets/option_rect_2.png")
option_button_rect = pygame.image.load(option_rect_res)
green_rect_res = resource_path("assets/option_rect_4.png")
green_button_rect = pygame.image.load(green_rect_res)
chat_rect_res = resource_path("assets/chat_rect.png")
chat_rect = pygame.image.load(chat_rect_res)

# ------------ Images -------------
tank_sand_up_res = resource_path('images/tanks/tank_sand_up.png')
tank_sand_up = pygame.image.load(tank_sand_up_res)
tank_sand_down_res = resource_path('images/tanks/tank_sand_down.png')
tank_sand_down = pygame.image.load(tank_sand_down_res)
tank_sand_left_res = resource_path('images/tanks/tank_sand_left.png')
tank_sand_left = pygame.image.load(tank_sand_left_res)
tank_sand_right_res = resource_path('images/tanks/tank_sand_right.png')
tank_sand_right = pygame.image.load(tank_sand_right_res)
tank_dark_up_res = resource_path('images/tanks/tank_dark_up.png')
tank_dark_up = pygame.image.load(tank_dark_up_res)
tank_dark_down = pygame.transform.flip(tank_dark_up, False, True)
tank_dark_left = pygame.transform.rotate(tank_dark_up, 90)
tank_dark_right = pygame.transform.rotate(tank_dark_up, -90)
tank_blue_up_res = resource_path('images/tanks/tank_blue_up.png')
tank_blue_up = pygame.image.load(tank_blue_up_res)
tank_blue_down = pygame.transform.flip(tank_blue_up, False, True)
tank_blue_left = pygame.transform.rotate(tank_blue_up, 90)
tank_blue_right = pygame.transform.rotate(tank_blue_up, -90)
tank_red_up_res = resource_path('images/tanks/tank_red_up.png')
tank_red_up = pygame.image.load(tank_red_up_res)
tank_red_down = pygame.transform.flip(tank_red_up, False, True)
tank_red_left = pygame.transform.rotate(tank_red_up, 90)
tank_red_right = pygame.transform.rotate(tank_red_up, -90)
tank_big_red_up_res = resource_path('images/tanks/tank_big_red_up.png')
tank_big_red_up = pygame.image.load(tank_big_red_up_res)
tank_big_red_down = pygame.transform.flip(tank_big_red_up, False, True)
tank_big_red_left = pygame.transform.rotate(tank_big_red_up, 90)
tank_big_red_right = pygame.transform.rotate(tank_big_red_up, -90)

# ------------ bullet ----------
bullet_dark_up_res = resource_path('images/tanks/bulletDarkUp.png')
bullet_dark_up = pygame.image.load(bullet_dark_up_res)
bullet_dark_down = pygame.transform.flip(bullet_dark_up, False, True)
bullet_dark_left = pygame.transform.rotate(bullet_dark_up, 90)
bullet_dark_right = pygame.transform.rotate(bullet_dark_up, -90)

# ------------ Shot flash ----------
flash_res = resource_path('images/flash/shotThin.png')
flash_up = pygame.image.load(flash_res)
flash_down = pygame.transform.flip(flash_up, False, True)
flash_left = pygame.transform.rotate(flash_up, 90)
flash_right = pygame.transform.rotate(flash_up, -90)

star_res = resource_path('images/icons/star.png')
star = pygame.image.load(star_res)
oil_res = resource_path('images/icons/oilSpill_large.png')
oil = pygame.image.load(oil_res)

# ------------ Fonts text -------------
tf2build_font1 = resource_path('resource/tf2build.ttf')
font_tf = pygame.font.Font(tf2build_font1, 13)
kyiv_font1 = resource_path('resource/KyivTypeTitling-Heavy2.ttf')
font_kyiv = pygame.font.Font(kyiv_font1, 15)
write_font1 = resource_path('resource/FirstTimeWriting-DOy8d.ttf')
font_write = pygame.font.Font(write_font1, 15)
font_info = pygame.font.Font(tf2build_font1, 15)
COLOR_INACTIVE = pygame.Color('lightskyblue1')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

# ----------- Icons images ----------
bomb_res = resource_path('images/icons/bomb_circle.png')
pic_bomb = pygame.image.load(bomb_res)
star_red_res = resource_path('images/icons/star_red.png')
star_red = pygame.image.load(star_red_res)
block_brick_res = resource_path('images/others/block_brick_100.png')
block_brick = pygame.image.load(block_brick_res)

# ----------- Explosion -----------
fire_res = resource_path('images/flash/explosion1.png')
fire2_res = resource_path('images/flash/explosion2.png')
fire3_res = resource_path('images/flash/explosion3.png')
fire4_res = resource_path('images/flash/explosion4.png')
fire5_res = resource_path('images/flash/explosion5.png')

explosion = [pygame.image.load(fire_res),
             pygame.image.load(fire2_res),
             pygame.image.load(fire3_res),
             pygame.image.load(fire4_res),
             pygame.image.load(fire5_res)]

# -------------- Sounds ---------
sms_res = resource_path('audio/sounds/sms.wav')
sms = pygame.mixer.Sound(sms_res)
build_res = resource_path('audio/sounds/build.wav')
build = pygame.mixer.Sound(build_res)
tank_fire_res = resource_path('audio/sounds/tank_shot.wav')
tank_fire = pygame.mixer.Sound(tank_fire_res)
tank_add_res = resource_path('audio/sounds/tank_add.wav')
tank_add = pygame.mixer.Sound(tank_add_res)
wall_break_res = resource_path('audio/sounds/wall_break.wav')
wall_break = pygame.mixer.Sound(wall_break_res)
tank_explosion_res = resource_path('audio/sounds/tank_explosion.wav')
tank_explosion = pygame.mixer.Sound(tank_explosion_res)
add_star_res = resource_path('audio/sounds/add_star.wav')
add_star = pygame.mixer.Sound(add_star_res)
take_up_star_res = resource_path('audio/sounds/take_up_star.wav')
take_up_star = pygame.mixer.Sound(take_up_star_res)
begin_res = resource_path('audio/sounds/begin.wav')
begin = pygame.mixer.Sound(begin_res)

tank_idle_res = resource_path('audio/sounds/tank_idle.wav')
tank_idle = pygame.mixer.Sound(tank_idle_res)
tank_moving_res = resource_path('audio/sounds/tank_moving.wav')
tank_moving = pygame.mixer.Sound(tank_moving_res)
# ------------ Time event ------------
clock = pygame.time.Clock()
# ------------ Tanks -------
tanks = []
bombs = []
explosions = []
red_stars = []
oils = []
tank_speed = 2  # int only
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
pure = (255, 0, 255)
white = (255, 255, 255)
azur = (0, 255, 255)
gray = (100, 100, 100)
colors = (red, blue, yellow, pure, white, azur, green, gray)
twitch_status = False
player = ""
aim = ""
info = ""
explosion_anim_count = 0
idle_sounds = []
moving_sounds = []
moving = False
all_t_moving = []
objects = []
title_size = 100


# ------- Game parameters save -------
def save_game_setting(screen_data_f):
    with open("assets/cfg/game_setting.cfg", 'w') as game_file:
        json.dump(screen_data_f, game_file)


def read_game_setting():
    with open("assets/cfg/game_setting.cfg", 'r') as game_file:
        return json.load(game_file)


WIDTH = read_game_setting()["width"]
HEIGHT = read_game_setting()["height"]
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Размер окна


def delete_all_out_screen(width, height):
    for tank in tanks:
        if tank.rect.x > width - 20 or tank.rect.y > height - 20:
            tanks.pop(tanks.index(tank))
    for bomb in bombs:
        if bomb.rect.x > width - 20 or bomb.rect.y > height - 20:
            bombs.pop(bombs.index(bomb))
    for red_star in red_stars:
        if red_star.rect.x > width - 20 or red_star.rect.y > height - 20:
            red_stars.pop(red_stars.index(red_star))
    for obj in objects:
        if obj.rect.x > width - 5 or obj.rect.y > height - 5:
            objects.pop(objects.index(obj))


# -------- Mouse --------
MOUSE_POS = pygame.mouse.get_pos()


def hi_score():
    global high_score_data
    for tank in tanks:
        if tank.count_kill > high_score_data['high_score']:
            high_score_data['high_score'] = tank.count_kill
            high_score_data['player_name'] = tank.name
    return high_score_data


def save_high_score(high_score_data_f):
    with open("assets/cfg/high_score.cfg", 'w') as high_score_file:
        json.dump(high_score_data_f, high_score_file)


def read_high_score():
    with open("assets/cfg/high_score.cfg") as high_score_file_r:
        return json.load(high_score_file_r)


high_score_data = read_high_score()


def save_channel_setting(channel_key_data_f):
    with open("assets/cfg/channel_setting.cfg", 'w') as channel_file:
        json.dump(channel_key_data_f, channel_file)


def read_channel_setting():
    with open("assets/cfg/channel_setting.cfg", 'r') as chanel_file:
        return json.load(chanel_file)


def save_option_setting(option_data_f, main_volume_f, walls_button, tank_chat):
    with open("assets/cfg/option_setting.cfg", 'w') as option_file:
        option_data_f['volume'] = main_volume_f
        option_data_f['brick_walls'] = walls_button
        option_data_f['tank_msg'] = tank_chat
        json.dump(option_data_f, option_file)


def read_option_setting():
    with open("assets/cfg/option_setting.cfg") as option_file:
        return json.load(option_file)


def save_option_green_bg(option_data_f, green_bg):
    with open("assets/cfg/option_setting.cfg", 'w') as option_file:
        option_data_f['green_bg'] = green_bg
        json.dump(option_data_f, option_file)


def read_option_green_bg():
    with open("assets/cfg/option_setting.cfg") as option_file:
        return json.load(option_file)


all_volume = read_option_setting()['volume']


def save_b_ground_setting(option_data_f, background_f):
    with open("assets/cfg/option_setting.cfg", 'w') as option_file:
        option_data_f['background'] = background_f
        json.dump(option_data_f, option_file)


def save_b_ground_show_chat(option_data_f, show_chat_f):
    with open("assets/cfg/option_setting.cfg", 'w') as option_file:
        option_data_f['show_chat'] = show_chat_f
        json.dump(option_data_f, option_file)


def check_difference(all_tank_moving):
    unique = set(all_tank_moving)
    if len(unique) >= 2:
        return True
    elif len(unique) == 1 and unique == {True}:
        return True
    elif len(unique) == 1 and unique == {False}:
        return False
    else:
        return False


class InputBox:

    def __init__(self, x, y, w, h, hide, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.hide = hide
        self.count_symbols = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print('Text added')
                elif event.key == pygame.K_v:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        self.text = pyperclip.paste()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Blit the text.
        if self.hide:
            hide_text = FONT.render('*' * len(self.text), True, self.color)
            screen.blit(hide_text, (self.rect.x + 5, self.rect.y + 5))
        else:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def set_hide_false(self):
        self.hide = False

    def set_hide_true(self):
        self.hide = True

    def get_text(self):
        return self.text


def resize_screen(even):
    global SCREEN
    if even.type == pygame.VIDEORESIZE:
        SCREEN = pygame.display.set_mode((even.w, even.h), pygame.RESIZABLE)
        if even.w < 1280 or even.h < 720 or even.w > 1280 or even.h > 720:
            even.w = 1280
            even.h = 720
        SCREEN = pygame.display.set_mode((even.w, even.h), pygame.RESIZABLE)
