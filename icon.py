from tank import *
from settings import *


class Icon:
    def __init__(self, x, y, c_icon, screen, volume):
        self.x = x
        self.y = y
        self.screen = screen
        self.icon = c_icon
        self.rect = self.icon.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.volume = volume
        sound_add_items(volume)

    def draw(self):
        self.screen.blit(self.icon, (self.x, self.y))


class Bomb(Icon):
    pass


class RedStar(Icon):
    pass


def spawn_bomb(time_bomb, random_x, random_y, volume):
    if time_bomb <= 0 and len(bombs) < 1:
        bombs.append(Bomb(random_x, random_y, pic_bomb, SCREEN, volume))
        for tank in tanks:
            rect_tank = tank.rect
            for bomb in bombs:
                rect_bomb = bomb.rect
                if rect_bomb.colliderect(rect_tank):
                    bombs.pop(bombs.index(bomb))


def spawn_red_star(time_red_star, random_x, random_y, volume):
    if time_red_star <= 0 and len(red_stars) < 1:
        red_stars.append(RedStar(random_x, random_y, star_red, SCREEN, volume))
        for tank in tanks:
            rect_tank = tank.rect
            for red_star in red_stars:
                rect_red_star = red_star.rect
                if rect_red_star.colliderect(rect_tank):
                    red_stars.pop(red_stars.index(red_star))
