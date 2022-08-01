import json
import time
import pygame
import sys
import os
import threading
from twitch_bot import *
import server
import random
from button import *
from objects import *
from keys_control import *
from twitch_control import *
from effects import *
from sounds import *
from settings import *
import webbrowser
import pygame.locals

# ----------------- Twitch message start ---------------------
thread_1 = threading.Thread(target=twitch_bot.run, args=())
thread_1.start()


# ---------------- Draw messages -----------------
def draw_msg(x, y, player_f, message_f):
    person = font_tf.render(f'{player_f}:  ', True, (230, 100, 250))
    msg = font_kyiv.render(f'{message_f}', True, ('Yellow'))
    SCREEN.blit(person, (x, y))
    SCREEN.blit(msg, (len(player_f) * 8 + 40, y))


# -------------- If long message, cut it -----------
def draw_chat():
    draw_msg(15, 80, twitch_bot.lst_chat[6], twitch_bot.lst_chat[7])
    draw_msg(15, 100, twitch_bot.lst_chat[4], twitch_bot.lst_chat[5])
    draw_msg(15, 120, twitch_bot.lst_chat[2], twitch_bot.lst_chat[3])
    draw_msg(15, 140, twitch_bot.lst_chat[0], twitch_bot.lst_chat[1])


# ---------- Draw kills info / high score --------
def draw_info(x, y, player_f, aim_f, info_f, name_score_f, hi_score_f):
    # ---- Kill / Destroy info
    player_font = font_info.render(f'{player_f} ', True, (100, 180, 150))
    info_font = font_info.render(f'{info_f}', True, (255, 0, 0))
    aim_font = font_info.render(f'{aim_f}', True, (150, 250, 200))
    SCREEN.blit(player_font, (x, y))
    SCREEN.blit(info_font, (len(player_f) * 8.5 + 35, y))
    SCREEN.blit(aim_font, (len(player_f) * 8.5 + len(info_f) * 8 + 55, y))
    # ---- Hi score ----
    max_score_font = font_info.render(f'HIGH SCORE: ', True, (100, 180, 250))
    name_score_font = font_info.render(f'{name_score_f} ', True, (100, 180, 150))
    hi_score_font = font_info.render(f'{hi_score_f}', True, (255, 0, 0))
    SCREEN.blit(max_score_font, (510, y - 10))
    SCREEN.blit(name_score_font, (440, y + 10))
    SCREEN.blit(hi_score_font, (len(name_score_f) * 8.5 + 470, y + 10))


# -------------------------------------------------------------------
# ------------------------------ GAME -------------------------------
def play(player_f, info_f, aim_f, moving_f):
    global RUN
    # -------- Set screen size ------
    WIDTH = read_game_setting()["width"]
    HEIGHT = read_game_setting()["height"]
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # ------- Parameters --------
    pygame.display.set_caption("Twitch tank 2022")
    time_bomb = time_bom_next = 12
    time_red_star = time_red_star_next = 10
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    try:
        file_background = read_option_setting()["background"]
        bg_game_res = resource_path(file_background)
        background_game_image = pygame.image.load(bg_game_res)
    except FileNotFoundError:
        pass
    except:
        print("Unsupported image format")
        pass
    green_background = read_option_green_bg()["green_bg"]  # True/False
    show_chat = read_option_setting()['show_chat']
    walls_button = read_option_setting()['brick_walls']
    all_volume = read_option_setting()['volume']
    tank_message = read_option_setting()['tank_msg']

    # ------- Create walls ------
    walls_max = (WIDTH // title_size * HEIGHT // title_size)
    wall_count = walls_max // 2 - len(tanks)
    if wall_count < 0:
        wall_count = 0
    if walls_button:
        objects.clear()
        create_walls(wall_count, WIDTH, HEIGHT)
    else:
        objects.clear()

    # -------- Sounds ----------
    sound_begin(all_volume / 1.5)

    while RUN:
        mouse_position = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        random_x = random.randint(0, WIDTH - 90)
        random_y = random.randint(0, HEIGHT - 90)
        user_input = pygame.key.get_pressed()
        random_color = colors[random.randint(0, len(colors) - 1)]
        oil_rotation = random.randint(0, 360)
        oil_size = random.randint(80, 110)
        NAME_SCORE = hi_score()['player_name']
        HI_SCORE = hi_score()['high_score']
        screen_data = {'width': WIDTH, 'height': HEIGHT}
        SCREEN.fill('Black')
        if not green_background:
            try:
                SCREEN.blit(background_game_image, (0, 0))
            except UnboundLocalError:
                pass
        else:
            pass

        # --------- TEST AFTER DELETE ------

        if user_input[pygame.K_g] and len(tanks) > 0:
            tanks.pop()

        # -------- Draw walls brick ----------
        for obj in objects:
            obj.draw()

        # ---- Sound idle ----
        sound_idle(all_volume / 2)

        # ---- Add class Sound moving ----
        add_class_sound_move(moving_f, all_volume / 2)

        # ---- Sound moving by Twitch ----
        check_tank_move()
        moving_f = check_difference(all_t_moving)
        all_t_moving.clear()

        # ---- Sound moving by keys ----
        if user_input[pygame.K_a]:
            moving_f = True
        elif user_input[pygame.K_s]:
            moving_f = True
        elif user_input[pygame.K_w]:
            moving_f = True
        elif user_input[pygame.K_d]:
            moving_f = True

        # -------- Draw explosion / oils -------
        for o in oils:
            o.oil_anim(oil)
        for expl in explosions:
            expl.explosion_anim()

        # ----- Twitch -----
        twitch_command = twitch_bot.command
        twitch_name = twitch_bot.chater
        time_move = twitch_bot.time_move

        # --------- Twitch control all tanks -----------
        twitch_command_movie(twitch_command, twitch_name, time_move, current_time, all_volume)

        # --------- Twitch build -------------
        twitch_command_build(twitch_command, twitch_name, walls_max, WIDTH, HEIGHT)

        # ----- Every tank ------
        tank_movie_by_commands(current_time, WIDTH, HEIGHT)

        # ------ Tank message -------
        for tank in tanks:
            if tank.name == twitch_bot.lst_chat[0] and tank_message:
                # tank.set_msg(twitch_bot.lst_chat[1])  # short message
                tank.set_msg(twitch_bot.full_msg)
                tank.set_time_msg(current_time)
            else:
                tank.set_msg('')

        # # -------- Check collision bullets, walls, tanks and destroy -------
        for tank in tanks:
            rect_tank = tank.rect
            for wall in objects:
                for bullet in tank.bullets:
                    if bullet.rect_bullet.colliderect(wall):
                        wall.damage(1)
                        tank.del_bullet()
            for other in tanks:
                rect_other = other.rect
                if rect_other.colliderect(rect_tank) and rect_other != rect_tank and tank.level >= other.level:
                    sound_tank_explosion(all_volume)
                    tanks.pop(tanks.index(rect_other))
                    oils.append(OilSpill(other.rect.x, other.rect.y, oil_rotation, oil_size))
                    if len(oils) > 10:
                        oils.pop(0)
                    player_f = tank.name
                    aim_f = other.name
                    info_f = "CRUSHED"
                    tank.count_kill += 1
                for bullet in tank.bullets:
                    if bullet.rect_bullet.colliderect(rect_other) and rect_tank != rect_other:
                        sound_tank_explosion(all_volume)
                        explosions.append(Explosion(other.rect.x, other.rect.y))
                        oils.append(OilSpill(other.rect.x, other.rect.y, oil_rotation, oil_size))
                        if len(explosions) > 10:
                            explosions.pop(0)
                        if len(oils) > 10:
                            oils.pop(0)
                        try:
                            tanks.pop(tanks.index(other))
                        except ValueError:
                            pass
                        tank.del_bullet()
                        player_f = tank.name
                        aim_f = other.name
                        info_f = "DESTROID"
                        tank.count_kill += 1

        # --- Add new tank by Q key ---
        add_tank_by_key(user_input, random_x, random_y, twitch_name, random_color, all_volume)

        # --------- Keys control for tank index 0 ----------
        keys_movie(user_input, current_time, all_volume)

        # --------- Build by r key ----------
        key_build_wall(user_input, walls_max, WIDTH, HEIGHT)

        # --------- TWITCH COMMANDS add tank -----------
        add_tank_by_twitch_command(random_x, random_y, twitch_name, twitch_command, random_color, all_volume)

        # ------------ Draw CHAT / INFO / HIGH SCORE / sound chat ------------
        if show_chat:
            sound_chat(all_volume)
            draw_chat()
            # SCREEN.blit(chat_rect, (0, 180))
            hi_score()
            draw_info(15, 20, player_f, aim_f, info_f, NAME_SCORE, HI_SCORE)
            # SCREEN.blit(info_rect, (-50, 0))

        # # ------------- Take red star --------------
        spawn_red_star(time_red_star, random_x, random_y, all_volume)
        for red_s in red_stars:
            red_s.draw()
            rect_star_red = red_s.rect
            for tank in tanks:
                rect_tank = tank.rect
                if rect_tank.colliderect(rect_star_red) and len(red_stars) > 0:
                    time_red_star = time_red_star_next
                    red_stars.pop(red_stars.index(red_s))
                    sound_take_up_star(all_volume)
                    if tank.level == 0:
                        tank.__class__ = TankBlue
                        tank.level = 1
                        tank.speed = tank_speed + 2
                    elif tank.level == 1:
                        tank.__class__ = TankDark
                        tank.level = 2
                        tank.speed = tank_speed + 3
                    elif tank.level == 2:
                        tank.__class__ = TankRed
                        tank.level = 3
                        tank.speed = tank_speed + 4
                    elif tank.level == 3:
                        tank.__class__ = TankBigRed
                        tank.level = 4
                        tank.speed = tank_speed + 4

        # # ------- take bomb ---------
        spawn_bomb(time_bomb, random_x, random_y, all_volume)
        for bomb in bombs:
            bomb.draw()
            rect_bomb = bomb.rect
            for tank in tanks:
                rect_tank = tank.rect
                if rect_tank.colliderect(rect_bomb):
                    time_bomb = time_bom_next
                    bombs.pop(bombs.index(bomb))
                    sound_take_up_star(all_volume)
                    for other in tanks:
                        if tanks.index(other) != tanks.index(tank):
                            tanks.pop(tanks.index(other))
                            tank.count_kill += 1
                            sound_tank_explosion(all_volume)
                            explosions.append(Explosion(other.rect.x, other.rect.y))
                            oils.append(OilSpill(other.rect.x, other.rect.y, oil_rotation, oil_size))
                            if len(explosions) > 10:
                                explosions.pop(0)
                            if len(oils) > 10:
                                oils.pop(0)

        # --- Game parameters ---
        clock.tick(FPS)  # frames/second
        pygame.display.update()

        # ----------- Event ---------
        for event in pygame.event.get():
            # ---------- Add/delete walls by mouse ---------
            if event.type == pygame.MOUSEBUTTONDOWN:
                walls_max = (WIDTH // title_size * HEIGHT // title_size)
                wall_count = walls_max // 2 - len(tanks)
                if event.button == 1 and len(objects) < wall_count:
                    add_wall_by_mouse(mouse_position)
                if event.button == 3:
                    del_wall(mouse_position)
                if event.button == 2:
                    del_all_walls()
            if event.type == pygame.QUIT:
                save_high_score(high_score_data)
                save_game_setting(screen_data)
                RUN = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_high_score(high_score_data)
                    save_game_setting(screen_data)
                    main_menu()
            if event.type == pygame.USEREVENT:
                time_bomb -= 1
                time_red_star -= 1

            # -------- Change video size if < HD size --------
            if event.type == pygame.VIDEORESIZE:
                # SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.w < 640 or event.h < 200:
                    event.w = 640
                    event.h = 200
                SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                WIDTH = event.w
                HEIGHT = event.h
                Tank.set_screen(WIDTH, HEIGHT)
                screen_data = {'width': WIDTH, 'height': HEIGHT}
                save_game_setting(screen_data)
                walls_max = (WIDTH // title_size * HEIGHT // title_size)
                wall_count = walls_max // 2 - len(tanks)
                objects.clear()

        # --------- Delete tank / bomb / wall / red_star out screen -----------
        delete_all_out_screen(WIDTH, HEIGHT)


# -------- Menu OPTION ---------
def options():
    global RUN
    global high_score_data

    all_volume = read_option_setting()['volume']
    show_chat = read_option_setting()['show_chat']
    walls_button = read_option_setting()['brick_walls']
    green_background = read_option_green_bg()["green_bg"]
    file_background = read_option_setting()["background"]
    tank_msg = read_option_setting()['tank_msg']
    option_data = {'volume': all_volume, 'background': file_background,
                   'green_bg': green_background, 'show_chat': show_chat,
                   'brick_walls': walls_button, "tank_msg": tank_msg}
    pygame.display.set_caption("Options")

    while RUN:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("Gray")

        # ---- Volume -----
        volume_text = get_font(25).render("Volume", True, "Black")
        volume_rect = volume_text.get_rect(center=(340, 60))
        SCREEN.blit(volume_text, volume_rect)

        button_minus = Button(image=button_rect, pos=(140, 120),
                              text_input="-", font=get_font(45), base_color="Blue",
                              hovering_color="Yellow")
        button_plus = Button(image=button_rect, pos=(540, 120),
                             text_input="+", font=get_font(45), base_color="Blue",
                             hovering_color="Yellow")

        pygame.draw.rect(SCREEN, 'Blue', (190, 105, 300 * all_volume, 30))
        pygame.draw.rect(SCREEN, 'black', (190, 105, 300, 30), 5)

        # ---------- Video tips -------------
        button_vieo_tips = Button(image=option_button_rect, pos=(900, 120),
                                  text_input="Video tips", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")

        # ------------- Green background -----------
        button_green_bg = Button(image=green_button_rect, pos=(500, 220),
                                 text_input="BACKGROUND", font=get_font(25), base_color="Blue",
                                 hovering_color="Yellow")
        button_green_bg_off = Button(image=green_button_rect, pos=(200, 220),
                                     text_input="BACKGROUND", font=get_font(25), base_color="Black",
                                     hovering_color="Yellow")

        # ---------- Change back ground -------------
        button_change_bg = Button(image=option_button_rect, pos=(900, 220),
                                  text_input="Chose back ground", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")

        # --------- Clear high score ----------
        button_clear_high_score = Button(image=option_button_rect, pos=(900, 520),
                                         text_input="Clear high score", font=get_font(25), base_color="Blue",
                                         hovering_color="Yellow")

        # ------- Show / hide chat -------
        button_show_chat = Button(image=green_button_rect, pos=(200, 320),
                                  text_input="CHAT ON", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")
        button_hide_chat = Button(image=green_button_rect, pos=(500, 320),
                                  text_input="CHAT OFF", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")

        # ------- ON / OFF walls -------
        button_walls_on = Button(image=green_button_rect, pos=(200, 420),
                                 text_input="WALLS ON", font=get_font(25), base_color="Blue",
                                 hovering_color="Yellow")
        button_walls_off = Button(image=green_button_rect, pos=(500, 420),
                                  text_input="WALLS OFF", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")

        # ------- ON / OFF tank message -------
        button_t_chat_on = Button(image=green_button_rect, pos=(200, 520),
                                  text_input="TANK CHAT", font=get_font(25), base_color="Blue",
                                  hovering_color="Yellow")
        button_t_chat_off = Button(image=green_button_rect, pos=(500, 520),
                                   text_input="TANK CHAT", font=get_font(25), base_color="Blue",
                                   hovering_color="Yellow")

        # ------ Back button ------
        OPTIONS_BACK = Button(image=back_rect, pos=(640, 660),
                              text_input="BACK", font=get_font(45), base_color="Black",
                              hovering_color="Yellow")

        # ------ Draw buttons -------
        for button in [button_minus, button_clear_high_score, button_plus,
                       OPTIONS_BACK, button_vieo_tips]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        # -------- Draw button green screen and button chose bg  if true -------
        if green_background:
            button_green_bg_off.changeColor(OPTIONS_MOUSE_POS)
            button_green_bg_off.update(SCREEN)
        elif not green_background:
            button_green_bg.changeColor(OPTIONS_MOUSE_POS)
            button_green_bg.update(SCREEN)
            button_change_bg.changeColor(OPTIONS_MOUSE_POS)
            button_change_bg.update(SCREEN)

        # ------- Draw / hide chat ----
        if show_chat:
            button_show_chat.changeColor(OPTIONS_MOUSE_POS)
            button_show_chat.update(SCREEN)
        else:
            button_hide_chat.changeColor(OPTIONS_MOUSE_POS)
            button_hide_chat.update(SCREEN)

        # ------- Draw buttons walls --------
        if walls_button:
            button_walls_on.changeColor(OPTIONS_MOUSE_POS)
            button_walls_on.update(SCREEN)
        else:
            button_walls_off.changeColor(OPTIONS_MOUSE_POS)
            button_walls_off.update(SCREEN)

        # -------- Draw buttons tank chat -------
        if tank_msg:
            button_t_chat_on.changeColor(OPTIONS_MOUSE_POS)
            button_t_chat_on.update(SCREEN)
        else:
            button_t_chat_off.changeColor(OPTIONS_MOUSE_POS)
            button_t_chat_off.update(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_option_setting(option_data, all_volume, walls_button, tank_msg)
                save_high_score(high_score_data)
                RUN = False
                pygame.quit()
            # -------- Back button --------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                    main_menu()
                # ---- Change volume buttons -----
                if button_plus.checkForInput(OPTIONS_MOUSE_POS):
                    all_volume += 0.1
                    if all_volume > 1:
                        all_volume = 1
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                if button_minus.checkForInput(OPTIONS_MOUSE_POS):
                    all_volume -= 0.1
                    if all_volume <= 0:
                        all_volume = 0
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                # ------------- Video tips ------------------
                if button_vieo_tips.checkForInput(OPTIONS_MOUSE_POS):
                    video_tips.preview()
                # ------ Clear high score -----
                if button_clear_high_score.checkForInput(OPTIONS_MOUSE_POS):
                    high_score_data = {"player_name": "Player name", "high_score": 0}
                    save_high_score(high_score_data)
                    # RUN = False
                    # pygame.quit()
                # ------- Green background ON/OFF ----------
                if button_green_bg.checkForInput(OPTIONS_MOUSE_POS):
                    green_background = True
                    save_option_green_bg(option_data, green_background)
                if button_green_bg_off.checkForInput(OPTIONS_MOUSE_POS):
                    green_background = False
                    save_option_green_bg(option_data, green_background)
                # ---------- Change back ground -------------
                if button_change_bg.checkForInput(OPTIONS_MOUSE_POS) and not green_background:
                    file_background = filedialog.askopenfilenames()
                    try:
                        save_b_ground_setting(option_data, file_background[0])
                    except IndexError:
                        pass
                # --------- Chat ON/OFF -------
                if button_show_chat.checkForInput(OPTIONS_MOUSE_POS):
                    show_chat = False
                    save_b_ground_show_chat(option_data, show_chat)
                if button_hide_chat.checkForInput(OPTIONS_MOUSE_POS):
                    show_chat = True
                    save_b_ground_show_chat(option_data, show_chat)
                # --------- Walls ON/OFF --------
                if button_walls_on.checkForInput(OPTIONS_MOUSE_POS):
                    walls_button = False
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                if button_walls_off.checkForInput(OPTIONS_MOUSE_POS):
                    walls_button = True
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                # -------- Tank chat -----------
                if button_t_chat_on.checkForInput(OPTIONS_MOUSE_POS):
                    tank_msg = False
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)
                if button_t_chat_off.checkForInput(OPTIONS_MOUSE_POS):
                    tank_msg = True
                    save_option_setting(option_data, all_volume, walls_button, tank_msg)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            resize_screen(event)


# -------- MAIN MENU ---------
def main_menu():
    global RUN
    global TWITCH
    global twitch_status

    idle_sounds.clear()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Main menu")
    begin.stop()
    while RUN:
        screen.blit(background_menu, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("TWITCH TANK", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        MENU_VERSION = get_font(25).render("V.1.0", True, "#b68f40")
        VERSION_RECT = MENU_VERSION.get_rect(center=(640, 650))

        twitch_ok_text = get_font(15).render("TWITCH CONNECTED", True, "#a81ac4")
        twitch_ok_rect = twitch_ok_text.get_rect(center=(180, 550))

        twitch_no_text = get_font(15).render("TWITCH NOT CONNECTED", True, "Red")
        twitch_no_rect = twitch_no_text.get_rect(center=(200, 550))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="Yellow")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4",
                                hovering_color="Yellow")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4",
                             hovering_color="Yellow")
        GET_CHANEL_BUTTON = Button(image=pygame.image.load("assets/Other Rect.png"), pos=(200, 600),
                                   text_input="SET CHANEL", font=get_font(25), base_color="#d7fcd4",
                                   hovering_color="Yellow")
        ABOUT_GAME_BUTTON = Button(image=pygame.image.load("assets/Other Rect.png"), pos=(1080, 600),
                                   text_input="ABOUT GAME", font=get_font(25), base_color="#d7fcd4",
                                   hovering_color="Yellow")
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(MENU_VERSION, VERSION_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, GET_CHANEL_BUTTON, ABOUT_GAME_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        if twitch_bot.lst_chat[0] != 'BOT':
            twitch_status = True
        if twitch_status:
            screen.blit(twitch_ok_text, twitch_ok_rect)
        else:
            screen.blit(twitch_no_text, twitch_no_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score_data)
                pygame.quit()
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play(player, info, aim, moving)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(player, info, aim, moving)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if GET_CHANEL_BUTTON.checkForInput(MENU_MOUSE_POS):
                    get_channel()
                if ABOUT_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    save_high_score(high_score_data)
                    RUN = False
                    pygame.quit()
            resize_screen(event)


# -------- Menu button get chanel ---------
def get_channel():
    global RUN
    global SCREEN

    run = True
    pygame.display.set_caption("Setting channel")
    input_channel = InputBox(540, 200, 240, 32, False)
    input_key = InputBox(540, 400, 240, 32, True)
    input_boxes = [input_channel, input_key]
    channel_key_data = read_channel_setting()

    while run:
        clock.tick(60)

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        channel_key_data['channel_name'] = input_channel.get_text()
        channel_key_data['oauth_key'] = input_key.get_text()

        SCREEN.fill((30, 30, 30))

        play_video_button = Button(image=green_button_rect, pos=(640, 80),
                                   text_input="Video tips", font=get_font(25),
                                   base_color="Blue", hovering_color="Yellow")
        play_video_button.changeColor(OPTIONS_MOUSE_POS)
        play_video_button.update(SCREEN)

        chanel_text = get_font(25).render("Twitch chanel:", True, "White")
        chanel_rect = chanel_text.get_rect(center=(640, 160))
        SCREEN.blit(chanel_text, chanel_rect)
        key_text_m = get_font(25).render("Twitch oauth key:", True, "White")
        key_rect = key_text_m.get_rect(center=(640, 360))
        SCREEN.blit(key_text_m, key_rect)

        restart_text = Button(image=info_rect, pos=(640, 500),
                              text_input="Save an restart the game!", font=get_font(25),
                              base_color="Blue", hovering_color="Yellow")
        restart_text.changeColor(OPTIONS_MOUSE_POS)
        if input_channel.get_text() != '' and input_key.get_text() != '':
            restart_text.update(SCREEN)

        get_key = Button(image=option_button_rect, pos=(640, 300),
                         text_input="Get oauth key!", font=get_font(25),
                         base_color="Blue", hovering_color="Yellow")

        get_key.changeColor(OPTIONS_MOUSE_POS)
        get_key.update(SCREEN)

        OPTIONS_BACK = Button(image=back_rect, pos=(640, 660),
                              text_input="BACK", font=get_font(45), base_color="Black",
                              hovering_color="Yellow")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        show_text_button = Button(image=green_button_rect, pos=(360, 420),
                                  text_input="Show key", font=get_font(25),
                                  base_color="Black", hovering_color="Yellow")

        show_text_button.changeColor(OPTIONS_MOUSE_POS)
        show_text_button.update(SCREEN)

        for box in input_boxes:
            box.update()
            box.draw(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score_data)
                run = False
                RUN = False
                pygame.quit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    run = False
                    main_menu()
                if show_text_button.checkForInput(OPTIONS_MOUSE_POS):
                    input_key.set_hide_false()
                if restart_text.checkForInput(OPTIONS_MOUSE_POS):
                    save_channel_setting(channel_key_data)
                    save_high_score(high_score_data)
                    run = False
                    RUN = False
                    pygame.quit()
                if get_key.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('http://twitchapps.com/tmi/', new=2)
                if play_video_button.checkForInput(OPTIONS_MOUSE_POS):
                    video_tips.preview()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu()
            resize_screen(event)


# -------- Menu button about game ---------
def about_game():
    global RUN
    global SCREEN
    run = True
    pygame.display.set_caption("About game")
    while run:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("Gray")

        OPTIONS_TEXT = get_font(25).render("Hello every one!", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 40))
        game_text1 = get_font(25).render("Write to chat:", True, "Black")
        game_rect1 = game_text1.get_rect(center=(640, 80))
        game_text2 = get_font(25).render("!tank      ", True, "Red")
        game_rect2 = game_text2.get_rect(center=(330, 130))
        game_text3 = get_font(25).render("!fire !shot", True, "Red")
        game_rect3 = game_text3.get_rect(center=(330, 170))
        game_text4 = get_font(25).render("!build     ", True, "Red")
        game_rect4 = game_text4.get_rect(center=(330, 210))
        game_text5 = get_font(25).render("!up        ", True, "Red")
        game_rect5 = game_text5.get_rect(center=(330, 250))
        game_text6 = get_font(25).render("!down 5    ", True, "Red")
        game_rect6 = game_text6.get_rect(center=(330, 290))
        game_text7 = get_font(25).render("!left 100  ", True, "Red")
        game_rect7 = game_text7.get_rect(center=(330, 330))
        game_text8 = get_font(25).render("!right 50  ", True, "Red")
        game_rect8 = game_text8.get_rect(center=(330, 370))
        sub_text2 = get_font(25).render("To add a tank", True, "Black")
        sub_rect2 = sub_text2.get_rect(center=(730, 130))
        sub_text3 = get_font(25).render("To shot      ", True, "Black")
        sub_rect3 = sub_text3.get_rect(center=(730, 170))
        sub_text4 = get_font(25).render("To build the wall", True, "Black")
        sub_rect4 = sub_text4.get_rect(center=(780, 210))
        sub_text5 = get_font(25).render("To turn up   ", True, "Black")
        sub_rect5 = sub_text5.get_rect(center=(730, 250))
        sub_text6 = get_font(25).render("To move down 0.5 second ", True, "Black")
        sub_rect6 = sub_text6.get_rect(center=(870, 290))
        sub_text7 = get_font(25).render("To move left 10 seconds ", True, "Black")
        sub_rect7 = sub_text7.get_rect(center=(870, 330))
        sub_text8 = get_font(25).render("To move right 5 seconds ", True, "Black")
        sub_rect8 = sub_text8.get_rect(center=(870, 370))
        thank_text1 = get_font(25).render("Special thank:", True, "Black")
        thank_rect1 = thank_text1.get_rect(center=(640, 420))
        creator_text = get_font(25).render("Created by:", True, "Black")
        creator_rect = thank_text1.get_rect(center=(680, 540))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(game_text1, game_rect1)
        SCREEN.blit(game_text2, game_rect2)
        SCREEN.blit(game_text3, game_rect3)
        SCREEN.blit(game_text4, game_rect4)
        SCREEN.blit(game_text5, game_rect5)
        SCREEN.blit(game_text6, game_rect6)
        SCREEN.blit(game_text7, game_rect7)
        SCREEN.blit(game_text8, game_rect8)
        SCREEN.blit(sub_text2, sub_rect2)
        SCREEN.blit(sub_text3, sub_rect3)
        SCREEN.blit(sub_text4, sub_rect4)
        SCREEN.blit(sub_text5, sub_rect5)
        SCREEN.blit(sub_text6, sub_rect6)
        SCREEN.blit(sub_text7, sub_rect7)
        SCREEN.blit(sub_text8, sub_rect8)
        SCREEN.blit(thank_text1, thank_rect1)
        SCREEN.blit(creator_text, creator_rect)

        thank_button_1 = Button(image=None, pos=(640, 460),
                                text_input="Kenney Vleugels", font=get_font(25), base_color="Blue",
                                hovering_color="Yellow")
        thank_button_1.changeColor(OPTIONS_MOUSE_POS)
        thank_button_1.update(SCREEN)

        thank_button_2 = Button(image=None, pos=(640, 500),
                                text_input="Baraltech", font=get_font(25), base_color="Blue",
                                hovering_color="Yellow")
        thank_button_2.changeColor(OPTIONS_MOUSE_POS)
        thank_button_2.update(SCREEN)

        creator_button = Button(image=None, pos=(640, 590),
                                text_input="VDK45", font=get_font(35), base_color="Blue",
                                hovering_color="Yellow")
        creator_button.changeColor(OPTIONS_MOUSE_POS)
        creator_button.update(SCREEN)

        donate_button = Button(image=None, pos=(1000, 590),
                               text_input="SUPPORT ME!", font=get_font(35), base_color="Blue",
                               hovering_color="Yellow")
        donate_button.changeColor(OPTIONS_MOUSE_POS)
        donate_button.update(SCREEN)

        twitch_button = Button(image=None, pos=(290, 590),
                               text_input="TWITCH", font=get_font(35), base_color="Blue",
                               hovering_color="Yellow")
        twitch_button.changeColor(OPTIONS_MOUSE_POS)
        twitch_button.update(SCREEN)

        OPTIONS_BACK = Button(image=back_rect, pos=(640, 660),
                              text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Yellow")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score_data)
                run = False
                RUN = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    run = False
                    main_menu()
                elif thank_button_1.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('https://www.kenney.nl/', new=2)
                elif thank_button_2.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('https://github.com/baraltech/', new=2)
                elif twitch_button.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('https://www.twitch.tv/vdk45', new=2)
                elif creator_button.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('https://github.com/VDK45', new=2)
                elif donate_button.checkForInput(OPTIONS_MOUSE_POS):
                    webbrowser.open('https://www.donationalerts.com/r/vdk45', new=2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu()
            resize_screen(event)


if __name__ == "__main__":
    main_menu()
    # play(player, info, aim, moving)
    print('Game has stopped')
    twitch_bot.TWITCH_RUN = False  # Stop twitch bot
    twitch_bot.send_mess('The game has stoped!')
    twitch_bot.send_mess('The game has stoped!')
    time.sleep(5)
    # server.server_stop()  # Stop socket server
    sys.exit()
