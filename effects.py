import random
from settings import *


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_count = 0

    def explosion_anim(self):
        if self.anim_count < 20:
            SCREEN.blit(explosion[self.anim_count//4], (self.x, self.y))
            self.anim_count += 1
        elif self.anim_count >= 20:  # frames
            del self


class OilSpill:
    def __init__(self, x, y, oil_rotation, oil_size):
        self.x = x
        self.y = y
        self.anim_count = 0
        self.rand_time = random.randint(60, 300)
        self.rotation = oil_rotation
        self.oil_size = oil_size

    def oil_anim(self, oil_f):
        if self.anim_count < self.rand_time:
            oil_r = pygame.transform.rotate(oil_f, self.rotation)
            oil_s = pygame.transform.scale(oil_r, (self.oil_size, self.oil_size))
            SCREEN.blit(oil_s, (self.x, self.y))
            self.anim_count += 1
        elif self.anim_count >= self.rand_time:  # frames
            del self
