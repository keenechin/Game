class Level():
    def __init__(self, gids):
        self.gids = gids
        self.color = (128, 148, 128)
        self.start_x = 50
        self.start_y = 50
        self.entities = []
        
    def render(self, surf):
        surf.fill(self.color)

        