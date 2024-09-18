import pygame

from src import Parameters

#class handling a ship in fleetbattle
class Ship:
    
    #@length: ship length in squares
    #@pos: graphical position of the ship, default is top left
    #@horizontal: orientation of the ship, default is horizontal
    def __init__(self, length = 1, pos = (0, 0), horizontal = True):
        self.length = length                #length in squares
        self.horizontal = horizontal        #orientation
        self.horizontalInit = horizontal    #initial orientation
        self.positionInit = pos             #initial position    
        self.Positions = [-1] * length      #positions occupied in grid (-1 is not placed)
        self.body = pygame.Rect((pos[0],    #graphical body of the ship
                                 pos[1],
                                 Parameters.SQUARE + horizontal * Parameters.SQUARE * (length - 1),
                                 Parameters.SQUARE + (1 - horizontal) * Parameters.SQUARE * (length - 1)))
            
    #resets ship values to default
    def reset(self):
        self.horizontal = self.horizontalInit
        self.Positions = [-1] * self.length
        self.body = pygame.Rect((self.positionInit[0],
                                 self.positionInit[1],
                                 Parameters.SQUARE + self.horizontal * Parameters.SQUARE * (self.length - 1),
                                 Parameters.SQUARE + (1 - self.horizontal) * Parameters.SQUARE * (self.length - 1)))
    
    #rotates the ship between horizontal and vertical
    def rotate(self):
        self.body.width, self.body.height = self.body.height, self.body.width
        self.horizontal = not self.horizontal
    
    #places the ship in grid position
    #@pos: grid position of first square of the ship 
    #return: True if placement is valid, False otherwise  
    def place(self, pos):
        line = pos // Parameters.N
        for i in range(self.length):
            if pos >= Parameters.N * Parameters.N:
                return False #placement is outside of grid (bottom)
            if self.horizontal and line != pos // Parameters.N:
                return False #placement is outside of grid (right)
            self.Positions[i] = pos
            if self.horizontal:
                pos += 1
            else:
                pos += Parameters.N
        return True
    
    #moves the ship body in a graphical grid based on its position
    #@pos: graphical location of the grid topleft (x, y)
    def anchorTo(self, pos):
        if self.Positions[0] >= 0: #ship positions must be filled
            self.body.x = pos[0] + Parameters.SQUARE * (self.Positions[0] % Parameters.N)
            self.body.y = pos[1] + Parameters.SQUARE * (self.Positions[0] // Parameters.N)