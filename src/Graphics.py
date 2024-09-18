import pygame
from pathlib import Path
from src import Parameters

#class handling all graphic elements of the game
class Graphics:
    
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode((Parameters.WIDTH, Parameters.HEIGHT))
        pygame.display.set_caption('FleetBattle')
        self.clock = pygame.time.Clock()
        #the grid showing player ships
        self.playerGrid = pygame.Rect((Parameters.MARGIN,
                                       Parameters.MARGIN,
                                       Parameters.N * Parameters.SQUARE,
                                       Parameters.N * Parameters.SQUARE))
        #the grid showing player attacks
        self.attackGrid = pygame.Rect((2 * Parameters.MARGIN + Parameters.N * Parameters.SQUARE,
                                       Parameters.MARGIN,
                                       Parameters.N * Parameters.SQUARE,
                                       Parameters.N * Parameters.SQUARE))
        #the area where ships are placed by the player. Equals the playerGrid with margin around
        self.placementArea = pygame.Rect((self.playerGrid.topleft[0] - Parameters.MARGIN,
                                          self.playerGrid.topleft[1] - Parameters.MARGIN,
                                          Parameters.N * Parameters.SQUARE + 2 * Parameters.MARGIN,
                                          Parameters.N * Parameters.SQUARE + 2 * Parameters.MARGIN))
        #before placement, ships are initially drawn in an invisible grid starting with position placementPos
        self.placementPos = 0
        #background image
        pathToImages = Path(__file__).parent.parent.joinpath('assets')
        self.bgTexture = pygame.image.load(pathToImages.joinpath('bg.png')).convert_alpha()
        self.bgTexture = pygame.transform.smoothscale(self.bgTexture,
                                                      (Parameters.N * Parameters.SQUARE,
                                                       Parameters.N * Parameters.SQUARE))
        #ship images are initialized based on ship length
        self.ShipTextures = {}
        for i in range (1, 6):
            self.ShipTextures[i] = pygame.image.load(pathToImages.joinpath(f'ship{i}.png')).convert_alpha()
            self.ShipTextures[i] = pygame.transform.smoothscale(self.ShipTextures[i],
                                                                (i * Parameters.SQUARE,
                                                                 Parameters.SQUARE))
        #explosion images
        self.HitTexture = {
            True : pygame.image.load(pathToImages.joinpath('explosion.png')).convert_alpha(),       #True: explosion on ship (hit)
            False : pygame.image.load(pathToImages.joinpath('explosion_sea.png')).convert_alpha()   #False: explosion at sea (miss)
        }
        for i in self.HitTexture:
            self.HitTexture[i] = pygame.transform.smoothscale(self.HitTexture[i],
                                                              (Parameters.SQUARE,
                                                               Parameters.SQUARE))
    
    def __del__(self):
        pygame.quit()
    
    def clearScreen(self):
        self.screen.fill((0, 0, 0))
    
    #draws all objects on screen
    def updateScreen(self):
        pygame.display.flip()

    #draws a N*N grid with background image
    #@offset: topleft point of the grid    
    def drawGrid(self, offset = (0, 0)):
        self.screen.blit(self.bgTexture, offset)
        for i in range(Parameters.N+1):
            #horizontal lines
            pygame.draw.line(self.screen,
                             (255, 255, 255),
                             (offset[0],
                              offset[1] + i * Parameters.SQUARE),
                             (offset[0] + Parameters.N * Parameters.SQUARE,
                              offset[1] + i * Parameters.SQUARE))
            #vertical lines
            pygame.draw.line(self.screen,
                             (255, 255, 255),
                             (offset[0] + i * Parameters.SQUARE,
                              offset[1]),
                             (offset[0] + i * Parameters.SQUARE,
                              offset[1] + Parameters.N * Parameters.SQUARE))
    
    def drawPlayerGrid(self):
        self.drawGrid(self.playerGrid.topleft)
        
    def drawEnemyGrid(self):
        self.drawGrid(self.attackGrid.topleft)

    #draws a hit image (explosion)
    #@isPlayer: True when player attacks, False when enemy attacks     
    #@pos: position of the attack on grid
    #@hit: True when hit, False when miss    
    def drawHit(self, isPlayer, pos, hit):
        offset = self.playerGrid.topleft
        if isPlayer:
            offset = self.attackGrid.topleft
        self.screen.blit(self.HitTexture[hit],
                         (offset[0] + Parameters.SQUARE * (pos % Parameters.N),
                          offset[1] + Parameters.SQUARE * (pos // Parameters.N)))
    
    #draws a ship image
    #@ship: object ship    
    def drawShip(self, ship):
        if ship.horizontal:
            self.screen.blit(self.ShipTextures[ship.length],
                             ship.body.topleft)
        else:
            self.screen.blit(pygame.transform.rotate(self.ShipTextures[ship.length],
                                                     -90),
                             ship.body.topleft)
    
    #gets attack position based on mouse position
    #return: position in attack grid, -1 if outside grid    
    def getAttackPosition(self):
        mousePos = pygame.mouse.get_pos()
        if self.attackGrid.collidepoint(mousePos):
            return ((mousePos[0] - self.attackGrid.x) // Parameters.SQUARE
                    + ((mousePos[1] - self.attackGrid.y) // Parameters.SQUARE) * Parameters.N)
        else:
            return -1   
        
    #gets grid position from ship rectangle
    #@body: ship body rectangle
    #return: grid position 
    def getGridPositionFromBody(self, body):
        return ((body.x - self.playerGrid.left) // Parameters.SQUARE
                + (body.y - self.playerGrid.top) * Parameters.N // Parameters.SQUARE)
    
    #checks whether a ship rectangle is fully in the placement area
    #@body: ship body rectangle 
    def isShipInPlacementArea(self, body):
        if self.placementArea.contains(body):
            return True
        else:
            return False
    
    #aligns a ship rectangle to the placement grid
    #@body: ship body rectangle 
    #return: aligned ship body rectangle    
    def alignToPlayerGrid(self, body):
        body.x = round((body.x - self.playerGrid.left) / Parameters.SQUARE) * Parameters.SQUARE + self.playerGrid.left
        body.y = round((body.y - self.playerGrid.top) / Parameters.SQUARE) * Parameters.SQUARE + self.playerGrid.top
        return body
    
    def getPlayerGrid(self):
        return self.playerGrid.topleft

    def getEnemyGrid(self):
        return self.attackGrid.topleft

    #assigns the next available spot for a ship for the initial ship drawing phase
    #ships are drawn in the attack grid with extra margins, the grid itself is not drawn in this phase
    #@size: size of the ship to be placed
    #return: next available position (x, y) that can fit the ship
    def getSpaceForShipSize(self, size):
        #if the ship doesn't fit in the current line, move to the leftmost position one line down
        if self.placementPos // Parameters.N != (self.placementPos + size) // Parameters.N:
            self.placementPos = (self.placementPos // Parameters.N + 1) * Parameters.N
        ret = (self.attackGrid.topleft[0]
               + Parameters.SQUARE
               * (self.placementPos % Parameters.N),
               self.attackGrid.topleft[1]
               + (Parameters.SQUARE + Parameters.MARGIN)
               * (self.placementPos // Parameters.N))
        self.placementPos += (size + 1)         
        return ret
    
    #displays a message in the center of the screen, below the grids
    #@message: the message to be displayed
    def textWindow(self, message):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(message, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.midtop = (Parameters.WIDTH // 2,
                           self.playerGrid.bottomright[0] + Parameters.MARGIN // 2)
        self.screen.blit(text, textRect)