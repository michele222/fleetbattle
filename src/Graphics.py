import pygame
from src.params import *

class Graphics:
    
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.placementGrid = pygame.Rect((0, 0, 2 * MARGIN + N * SQUARE, 2 * MARGIN + N * SQUARE))
        self.playerGrid = pygame.Rect((MARGIN, MARGIN, N * SQUARE, N * SQUARE))
        self.attackGrid = pygame.Rect((2 * MARGIN + N * SQUARE, MARGIN, N * SQUARE, N * SQUARE))
    
    def __del__(self):
        pygame.quit()

    def drawGrid(self, offset = (0, 0)): #draw placement grid
        for i in range(N+1):
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0], offset[1] + i * SQUARE), (offset[0] + N * SQUARE, offset[1] + i * SQUARE))
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0] + i * SQUARE, offset[1]), (offset[0] + i * SQUARE, offset[1] + N * SQUARE))
        
    def drawPlayerGrid(self):
        self.drawGrid((MARGIN, MARGIN))
        
    def drawEnemyGrid(self):
        self.drawGrid((MARGIN * 2 + N * SQUARE, MARGIN))

    def drawHit(self, isPlayer, pos, hit):
        offset = self.playerGrid.topleft
        if isPlayer is True:
            offset = self.attackGrid.topleft
        if hit:
            pygame.draw.rect(self.screen, (255, 0, 0), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))
    
    def clearScreen(self):
        self.screen.fill((0, 0, 0))
        
    def updateScreen(self):
        pygame.display.flip()
        
    def drawShip(self, body):
        pygame.draw.rect(self.screen, (0, 255, 0), body)
        
    def playerAttacked(self, mousePos):
        if self.attackGrid.collidepoint(mousePos):
            return True
        else:
            return False
        
    def getAttackPosition(self, mousePos):
        return (mousePos[0] - self.attackGrid.x) // SQUARE + ((mousePos[1] - self.attackGrid.y) // SQUARE) * N
    
    def isShipInPlacementGrid(self, body):
        if self.placementGrid.contains(body):
            return True
        else:
            return False
    
    def alignToPlacementGrid(self, body):
        body.x = round((body.x - MARGIN) / SQUARE) * SQUARE + MARGIN
        body.y = round((body.y - MARGIN) / SQUARE) * SQUARE + MARGIN
        return body

    def getGridPositionFromBody(self, body):
        return (body.x - MARGIN) // SQUARE + (body.y - MARGIN) * N // SQUARE