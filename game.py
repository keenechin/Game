from gameloop import GameLoop, id_generator
from world import Level
from player import Player
        
gid = id_generator()
level = Level(gid)
loop = GameLoop(scene=level)
player = Player(next(gid), level.start_x, level.start_y)
loop.register(player)
for entity in level.entities:
    loop.register(entity)
loop.run()