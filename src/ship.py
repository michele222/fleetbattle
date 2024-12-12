import pygame

from src import parameters

#class handling a ship in fleetbattle
class Ship:
    
    #@length: ship length in squares
    #@pos: graphical position of the ship, default is top left
    #@horizontal: orientation of the ship, default is horizontal
    def __init__(self, length = 1, pos = (0, 0), horizontal = True):
        self.length = length                #length in squares
        self.horizontal = horizontal        #orientation
        self.horizontal_init = horizontal    #initial orientation
        self.position_init = pos             #initial position
        self.positions = [None] * length      #positions occupied in grid
        self.body = pygame.Rect((pos[0],    #graphical body of the ship
                                 pos[1],
                                 parameters.SQUARE + horizontal * parameters.SQUARE * (length - 1),
                                 parameters.SQUARE + (1 - horizontal) * parameters.SQUARE * (length - 1)))
            
    #resets ship values to default
    def reset(self):
        self.horizontal = self.horizontal_init
        self.positions = [None] * self.length
        self.body = pygame.Rect((self.position_init[0],
                                 self.position_init[1],
                                 parameters.SQUARE + self.horizontal * parameters.SQUARE * (self.length - 1),
                                 parameters.SQUARE + (1 - self.horizontal) * parameters.SQUARE * (self.length - 1)))
    
    #rotates the ship between horizontal and vertical
    def rotate(self):
        self.body.width, self.body.height = self.body.height, self.body.width
        self.horizontal = not self.horizontal
    
    #places the ship in grid position
    #@pos: grid position of first square of the ship 
    #return: True if placement is valid, False otherwise  
    def place(self, pos):
        for i in range(self.length):
            if pos[0] >= parameters.N[0] or pos[1] >= parameters.N[1]:
                return False #placement is outside of grid
            self.positions[i] = pos
            if self.horizontal:
                pos = (pos[0] + 1, pos[1])
            else:
                pos = (pos[0], pos[1] + 1)
        return True
    
    #moves the ship body in a graphical grid based on its position
    #@pos: graphical location of the grid topleft (x, y)
    def anchor_to(self, pos):
        if len(self.positions[0]) > 0: #ship positions must be filled
            self.body.x = pos[0] + parameters.SQUARE * self.positions[0][0]
            self.body.y = pos[1] + parameters.SQUARE * self.positions[0][1]