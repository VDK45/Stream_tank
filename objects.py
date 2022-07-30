from tank import *
from settings import *


class Icon:
    def __init__(self, px, py, c_icon, screen, volume):
        self.x = px
        self.y = py
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


# ------ Wall blocks -----
class WallBrick:
    def __init__(self, px, py, wall_block):
        self.x = px
        self.y = py
        self.wall = wall_block
        self.rect = self.wall.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        objects.append(self)
        self.type = 'block'
        self.hp = 1
        sound_build_wall(all_volume)

    def update(self):
        pass

    def draw(self):
        SCREEN.blit(self.wall, (self.x, self.y))

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            sound_wall_break(all_volume)
            objects.remove(self)


# -------- Create random walls ----------
def create_walls(count_w, width, height, title=title_size):
    for _ in range(count_w):
        while True:
            if len(objects) > count_w:
                objects.pop()
            x = randint(0, width // title - 1) * title
            y = randint(0, height // title - 1) * title
            rect = pygame.Rect(x, y, title, title)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    fined = True
            for tank in tanks:
                if rect.colliderect(tank.rect):
                    fined = True
            if not fined:
                break
        sound_build_wall(all_volume)
        WallBrick(x, y, block_brick)


# -------- Add wall --------
def add_wall_by_mouse(position):
    WallBrick(position[0], position[1], block_brick)
    sound_build_wall(all_volume)


# -------- Delete wall -------
def del_wall(position):
    for wall in objects:
        if position[0] in range(wall.rect.left, wall.rect.right) \
                and position[1] in range(wall.rect.top, wall.rect.bottom):
            wall.damage(1)


# --------- Delete all walls -------
def del_all_walls():
    objects.clear()



