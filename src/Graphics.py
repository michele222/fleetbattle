import pygame
import Parameters
import Ship

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
        self.bgTexture = pygame.image.load(r'assets\bg.png').convert_alpha()
        self.bgTexture = pygame.transform.smoothscale(self.bgTexture, (Parameters.N * Parameters.SQUARE, Parameters.N * Parameters.SQUARE))
        self.ShipTextures = {}
        for i in range (1, 6):
            self.ShipTextures[i] = pygame.image.load(f'assets\ship{i}.png').convert_alpha()
            self.ShipTextures[i] = pygame.transform.smoothscale(self.ShipTextures[i], (i * Parameters.SQUARE, Parameters.SQUARE))
        self.HitTexture = {
            True : pygame.image.load('assets\explosion.png').convert_alpha(),
            False : pygame.image.load('assets\explosion_sea.png').convert_alpha()
        }
        for i in self.HitTexture:
            self.HitTexture[i] = pygame.transform.smoothscale(self.HitTexture[i], (Parameters.SQUARE, Parameters.SQUARE))
    
    def __del__(self):
        pygame.quit()

    def drawGrid(self, offset = (0, 0)): #draw placement grid
        self.screen.blit(self.bgTexture, offset)
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
        #pygame.draw.rect(self.screen, color, (offset[0] + Parameters.SQUARE * (pos % Parameters.N), offset[1] + Parameters.SQUARE * (pos // Parameters.N), Parameters.SQUARE, Parameters.SQUARE))
        self.screen.blit(self.HitTexture[hit], (offset[0] + Parameters.SQUARE * (pos % Parameters.N), offset[1] + Parameters.SQUARE * (pos // Parameters.N)))
    
    def clearScreen(self):
        self.screen.fill((0, 0, 0))
        
    def updateScreen(self):
        pygame.display.flip()
        
    def drawShip(self, ship):
        #pygame.draw.rect(self.screen, (0, 255, 0), ship.body)
        if ship.horizontal:
            self.screen.blit(self.ShipTextures[ship.length], ship.body.topleft)
        else:
            self.screen.blit(pygame.transform.rotate(self.ShipTextures[ship.length], -90), ship.body.topleft)
        
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
        text = font.render(message, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.midtop = (Parameters.WIDTH // 2, self.playerGrid.bottomright[0] + Parameters.MARGIN // 2)
        self.screen.blit(text, textRect)