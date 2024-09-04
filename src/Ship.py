import pygame
from src.params import *

class Ship:
    
    def __init__(self, length = 1, pos = (0, 0), horizontal = True):
        self.length = length
        self.alive = True
        self.horizontal = horizontal
        self.horizontalInit = horizontal
        self.Positions = [-1] * length
        self.Hit = [False] * length
        self.body = pygame.Rect((pos[0], pos[1], SQUARE + horizontal * SQUARE * (length - 1), SQUARE + (1 - horizontal) * SQUARE * (length - 1)))
        self.positionInit = pos
    
    def reset(self):
        self.horizontal = self.horizontalInit
        self.body = pygame.Rect((self.positionInit[0], self.positionInit[1], SQUARE + self.horizontal * SQUARE * (self.length - 1), SQUARE + (1 - self.horizontal) * SQUARE * (self.length - 1)))
        self.Positions = [-1] * self.length
        
    def rotate(self):
        self.body.width, self.body.height = self.body.height, self.body.width
        self.horizontal = not self.horizontal
        
    def place(self, pos):
        line = pos // N
        for i in range(self.length):
            if pos >= N * N:
                return False #if placement is outside of grid (bottom)
            if self.horizontal and line != pos // N:
                return False #if placement is outside of grid (right)
            self.Positions[i] = pos
            if self.horizontal:
                pos += 1
            else:
                pos += N
        return True
    
    def alignTo(self, pos):
        if self.Positions[0] >= 0:
            self.body.x = pos[0] + SQUARE * (self.Positions[0] % N)
            self.body.y = pos[1] + SQUARE * (self.Positions[0] // N)