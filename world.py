import random
class Level():
    def __init__(self, gids):
        self.gids = gids
        self.color = [128, 168, 128]
        self.target_red = 128
        self.start_x = 50
        self.start_y = 50
        self.entities = []
        self.time = 0
        
    def update(self, dt):
        self.time = self.time + dt
        if self.time >= 60:
            self.time = 0
        if int(self.time) % 30 == 0:
            self.target_red = 128 + 5 * random.randint(-1, 1)
        
        red = self.color[0]
        if self.target_red > red:
            self.color[0] += 1
        if self.target_red < red:
            self.color[0] -= 1

    def render(self, surf, dt):
        surf.fill(tuple(self.color))

        