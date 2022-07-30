import random
from settings import *


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_count = 0

    def explosion_anim(self):
        if self.anim_count < 5:
            SCREEN.blit(explosion[self.anim_count], (self.x, self.y))
            self.anim_count += 1
        elif self.anim_count >= 5:  # frames
            del self


class OilSpill:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_count = 0
        self.rand_time = random.randint(60, 300)

    def oil_anim(self):
        if self.anim_count < self.rand_time:
            SCREEN.blit(oil, (self.x, self.y))
            self.anim_count += 1
        elif self.anim_count >= self.rand_time:  # frames
            del self
