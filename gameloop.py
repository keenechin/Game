import pygame
import time

class GameLoop():
    def __init__(self, scene, screen_size=(640, 480), fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.scene = scene
        self.entities = dict()
        self.listeners = {
            pygame.QUIT : [(-1, self.shutdown, (None,))]
        }
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

    def shutdown(self, event, *args):
        self.running = False
    
    def run(self):
        self.target_fps = 60
        dt = self.target_fps / self.fps
        while self.running:
            start = time.time()
            for event in pygame.event.get():
                if event.type in self.listeners.keys():
                    for response in self.listeners[event.type]:
                        gid, func, args = response
                        # print((gid, func, args))
                        func(event, *args)

            self.scene.update(dt)
            for entity in self.entities.values():
                entity.update(dt)
            
            self.scene.render(self.screen, dt)
            for entity in self.entities.values():
                entity.render(self.screen, dt)

            pygame.display.update()
            self.clock.tick(self.fps)
            dt = (time.time() - start) * self.target_fps

        pygame.quit()
             
    def register(self, gameObject):
        self.entities[gameObject.id] = gameObject
        for event_type, response in gameObject.behaviors.items():
            if event_type not in self.listeners.keys():
                self.listeners[event_type] = []
            func, args = response
            self.listeners[event_type].append((gameObject.id, func, args))
        
    def unregister(self, gameObject):
        self.entities.pop(gameObject.id)
        for event_type in gameObject.behaviors.keys():
            to_remove = []
            for i, response in enumerate(self.listeners[event_type]):
                id, _, _ = response
                if id == gameObject.id:
                    to_remove.append(i)
            to_remove = set(to_remove)
            self.listeners[event_type] = [response for i, response in enumerate(self.listeners[event_type]) if i not in to_remove]
                

def id_generator():
    i = 0
    while True:
        yield i
        i = i + 1

