import pygame
from pygame import K_w, K_a, K_s, K_d
from enum import Enum
import numpy as np


class MovementState(Enum):
    STOPPED = 0
    ACCEL = 1
    TOP_SPEED = 2


class MovementComponent:
    
    def __init__(self, entity):
        self.state = MovementState.STOPPED
        self.dir = np.array([1, 0])
        self.base_speed = 1
        self.speed = 0
        self.top_speed = 5
        self.acc_period = 60
        self.acc_time = 0
        self.parent = entity
        self.move_keys = set([K_w, K_a, K_s, K_d])

    def stop_moving(self):
        self.speed = 0
        self.acc_time = 0
        self.state = MovementState.STOPPED

    def handle_keydown(self, event, _):
        if event.key not in self.move_keys:
            return
        if event.key == K_w:
            self.dir[1] -= 1
        if event.key == K_a:
            self.dir[0] -= 1
        if event.key == K_s:
            self.dir[1] += 1
        if event.key == K_d:
            self.dir[0] += 1
        
        mag = (self.dir[0]**2 + self.dir[1]**2)**0.5
        if mag == 0:
            self.stop_moving()
            return 
        self.dir = self.dir/mag
        self.state = MovementState.ACCEL

    def handle_keyup(self, event, _):
        if event.key not in self.move_keys:
            return
        if event.key == pygame.K_w:
            self.dir[1] = 0 
        if event.key == pygame.K_a:
            self.dir[0] = 0
        if event.key == pygame.K_s:
            self.dir[1] = 0 
        if event.key == pygame.K_d:
            self.dir[0] = 0

        pressed = pygame.key.get_pressed()
        for key in self.move_keys:
            if pressed[key]:
                return
        self.stop_moving()

    def update(self, dt):
        if self.state == MovementState.ACCEL:
            init_period = self.acc_period // 12
            init_acc = 40
            if self.acc_time <= init_period: 
                self.speed = self.base_speed * init_acc * (self.acc_time/self.acc_period)
            else:
                self.speed = self.base_speed * init_acc * (init_period/self.acc_period) + \
                             self.base_speed * init_acc/5 * ((self.acc_time-init_period)/self.acc_period)
            self.acc_time += dt
            
        if self.speed >= self.top_speed:
            self.speed = self.top_speed
            self.state = MovementState.TOP_SPEED
        
        self.parent.x += self.dir[0] * self.speed
        self.parent.y += self.dir[1] * self.speed


class Player():
    def __init__(self, id, x, y):
        self._id = id 
        self.x = x
        self.y = y
        self.move_component = MovementComponent(self)

        self.base_color = (50, 50, 50)
        self.color = self.base_color
        self.size = 30
        self.trail = []

        self._behaviors = self.behaviors
    
    @property
    def id(self):
        return self._id

    @property
    def behaviors(self):
        behaviors = {
                pygame.KEYDOWN : (self.move_component.handle_keydown, (None,)),
                pygame.KEYUP : (self.move_component.handle_keyup, (None,))
            }
        return behaviors

    def update(self, dt):
        self.move_component.update(dt)

    def render(self, screen, dt):
        color = self.color
        radius = self.size/2
        pygame.draw.circle(screen, color, (self.x, self.y), radius)
