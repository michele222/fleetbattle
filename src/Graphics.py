import pygame
import Parameters

class Graphics:
    
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode((Parameters.WIDTH, Parameters.HEIGHT))
        pygame.display.set_caption('FleetBattle')
        self.clock = pygame.time.Clock()
        self.placementGrid = pygame.Rect((0, 0, 2 * Parameters.MARGIN + Parameters.N * Parameters.SQUARE, 2 * Parameters.MARGIN + Parameters.N * Parameters.SQUARE))
        self.playerGrid = pygame.Rect((Parameters.MARGIN, Parameters.MARGIN, Parameters.N * Parameters.SQUARE, Parameters.N * Parameters.SQUARE))
        self.attackGrid = pygame.Rect((2 * Parameters.MARGIN + Parameters.N * Parameters.SQUARE, Parameters.MARGIN, Parameters.N * Parameters.SQUARE, Parameters.N * Parameters.SQUARE))
        self.placementPos = 0
    
    def __del__(self):
        pygame.quit()

    def drawGrid(self, offset = (0, 0)): #draw placement grid
        for i in range(Parameters.N+1):
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0], offset[1] + i * Parameters.SQUARE), (offset[0] + Parameters.N * Parameters.SQUARE, offset[1] + i * Parameters.SQUARE))
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0] + i * Parameters.SQUARE, offset[1]), (offset[0] + i * Parameters.SQUARE, offset[1] + Parameters.N * Parameters.SQUARE))
        
    def drawPlayerGrid(self):
        self.drawGrid(self.playerGrid.topleft)
        
    def drawEnemyGrid(self):
        self.drawGrid(self.attackGrid.topleft)

    def drawHit(self, isPlayer, pos, hit):
        offset = self.playerGrid.topleft
        if isPlayer is True:
            offset = self.attackGrid.topleft
        color = (0, 0, 255)
        if hit:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color, (offset[0] + Parameters.SQUARE * (pos % Parameters.N), offset[1] + Parameters.SQUARE * (pos // Parameters.N), Parameters.SQUARE, Parameters.SQUARE))
    
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
        return (mousePos[0] - self.attackGrid.x) // Parameters.SQUARE + ((mousePos[1] - self.attackGrid.y) // Parameters.SQUARE) * Parameters.N
    
    def isShipInPlacementGrid(self, body):
        if self.placementGrid.contains(body):
            return True
        else:
            return False
    
    def alignToPlacementGrid(self, body):
        body.x = round((body.x - Parameters.MARGIN) / Parameters.SQUARE) * Parameters.SQUARE + Parameters.MARGIN
        body.y = round((body.y - Parameters.MARGIN) / Parameters.SQUARE) * Parameters.SQUARE + Parameters.MARGIN
        return body

    def getGridPositionFromBody(self, body):
        return (body.x - Parameters.MARGIN) // Parameters.SQUARE + (body.y - Parameters.MARGIN) * Parameters.N // Parameters.SQUARE
    
    def getPlayerGrid(self):
        return self.playerGrid.topleft

    def getEnemyGrid(self):
        return self.attackGrid.topleft

    def getSpaceForShipSize(self, size):
        if self.placementPos // Parameters.N != (self.placementPos + size) // Parameters.N:
            self.placementPos = (self.placementPos // Parameters.N + 1) * Parameters.N
        ret = (self.attackGrid.topleft[0] + Parameters.SQUARE * (self.placementPos % Parameters.N), self.attackGrid.topleft[1] + (Parameters.SQUARE + Parameters.MARGIN) * (self.placementPos // Parameters.N))
        self.placementPos += (size + 1)         
        return ret
            
    
    def textWindow(self, message):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(message, True, (255, 255, 255), (10, 10, 10))
        textRect = text.get_rect()
        textRect.center = (Parameters.WIDTH // 2, Parameters.HEIGHT // 2)
        self.screen.blit(text, textRect)