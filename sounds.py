import twitch_bot
from settings import *


class IdleSound:
    def __init__(self, tank_idl, volume):
        self.tank_idle = tank_idl
        self.volume = volume
        self.tank_idle.set_volume(self.volume / 3)
        self.tank_idle.play(-1)

    def __del__(self):
        self.tank_idle.stop()


class MovingSound:
    def __init__(self, tank_mov, volume):
        self.tank_moving = tank_mov
        self.volume = volume
        self.tank_moving.set_volume(self.volume)
        self.tank_moving.play(-1)

    def __del__(self):
        self.tank_moving.stop()


def sound_chat(volume):
    try:
        if twitch_bot.sound and twitch_bot.command[0] != '!' and twitch_bot.message[0:8] != 'tmi.twit':
            sms.set_volume(volume/2)
            sms.play()
    except IndexError:
        pass


def sound_tank_fire(volume):
    tank_fire.set_volume(volume/2)
    tank_fire.play()


def sound_tank_add(volume):
    tank_add.set_volume(volume/3)
    tank_add.play()


def sound_tank_explosion(volume):
    tank_explosion.set_volume(volume/2)
    tank_explosion.play()


def sound_add_items(volume):
    add_star.set_volume(volume/2)
    add_star.play()


def sound_build_wall(volume):
    build.set_volume(volume/8)
    build.play()


def sound_take_up_star(volume):
    take_up_star.set_volume(volume/2)
    take_up_star.play()


def sound_wall_break(volume):
    wall_break.set_volume(volume*1)
    wall_break.play()


def sound_begin(volume):
    begin.set_volume(volume/2)
    begin.stop()
    begin.play()


def sound_idle(volume):
    if len(tanks) > 0 and len(idle_sounds) < 1:
        idle_sounds.append(IdleSound(tank_idle, volume/2))
    if len(tanks) <= 0:
        try:
            idle_sounds.pop()
        except IndexError:
            pass


def add_class_sound_move(mov, volume):
    if mov and len(tanks) > 0 and len(moving_sounds) < 1:
        moving_sounds.append(MovingSound(tank_moving, volume/2))
    if len(tanks) <= 0 or not mov:
        try:
            moving_sounds.pop()
        except IndexError:
            pass


def check_tank_move():
    for tank in tanks:
        rect_tank = tank.rect
        tank_move = tank.get_m_moving()
        if tank_move[0] or tank_move[1] or tank_move[2] or tank_move[3]:
            t_moving = True
            all_t_moving.append(t_moving)
        else:
            t_moving = False
            all_t_moving.append(t_moving)
