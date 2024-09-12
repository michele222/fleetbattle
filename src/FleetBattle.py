import pygame
import random
import Parameters
from src.Graphics import Graphics
from src.Ship import Ship
from src.AttackProbabilityMatrix import AttackProbabilityMatrix

#main class running the game
class FleetBattle:
    
    def __init__(self):
        self.graphics = Graphics()
        self.Ships = []             #player ships
        self.ShipsEnemy = []        #enemy ships
        self.playerPositions = []   #positions occupied by player ships
        self.enemyPositions = []    #positions occupied by enemy ships
        self.phase = 1              #game phase
        for i in Parameters.SHIPS:
            self.Ships.append(Ship(i, self.graphics.getSpaceForShipSize(i)))
            self.ShipsEnemy.append(Ship(i))
    
    #manual placement of ships by player
    def placeShipsPlayer(self):
        if self.phase == 0:
            return
        placedShips = 0
        holdShip = -1 #no ship selected: -1, ship selected: ship id
        #ship placement phase
        while self.phase == 1:
            self.graphics.clearScreen()
            self.graphics.drawPlayerGrid()
            for ship in self.Ships:
                self.graphics.drawShip(ship)

            mouseKey = pygame.mouse.get_pressed()
            if mouseKey[0]: #left click
                mousePos = pygame.mouse.get_pos()
                #ship is selected with mouse
                if holdShip < 0:
                    for i in range(len(self.Ships)):
                        if self.Ships[i].body.collidepoint(mousePos):
                            holdShip = i
                #selected ship follows mouse
                if holdShip >= 0:
                    self.Ships[holdShip].body.center = mousePos
            #selected ship has been released by mouse
            elif holdShip >= 0:
                #selected ship has been released inside the placement area
                if self.graphics.isShipInPlacementArea(self.Ships[holdShip].body):
                    self.Ships[holdShip].body = self.graphics.alignToPlayerGrid(self.Ships[holdShip].body)
                    #this is a ship not placed before
                    if self.Ships[holdShip].Positions[0] < 0:
                        placedShips += 1
                    gridPosition = self.graphics.getGridPositionFromBody(self.Ships[holdShip].body)
                    self.Ships[holdShip].place(gridPosition)
                    #check collisions with other ships
                    for i in range(len(self.Ships)):
                        #in case of collision, the ship is placed back in its default position outside of the grid
                        if i != holdShip and any(j in self.Ships[holdShip].Positions for j in self.Ships[i].Positions):
                           self.Ships[holdShip].reset() 
                           placedShips -= 1
                           break           
                else: #ship released outside of placement grid
                    #this is a ship that was previously placed
                    if self.Ships[holdShip].Positions[0] >= 0:
                        placedShips -= 1
                    self.Ships[holdShip].reset()
                holdShip = -1
            
            #all ships are placed
            if placedShips == len(self.Ships):
                self.phase = 2
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                #right mouse button release on a selected ship rotates the ship
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and holdShip >= 0:
                    self.Ships[holdShip].rotate()
            
            self.graphics.updateScreen()
            self.graphics.clock.tick(60)

        for i in range(len(self.Ships)):
            self.playerPositions.extend(self.Ships[i].Positions)
    
    #random placement of ships in grid
    #@player: defines whether player or enemy ships are randomly placed
    def placeShipsRandomly(self, player = True):
        if self.phase == 0:
            return
        placedShips = 0
        Ships = []
        positions = []
        if player is True:
            Ships = self.Ships
            positions = self.playerPositions
        else:
            Ships = self.ShipsEnemy    
            positions = self.enemyPositions
        for i in range(len(Ships)):
            while placedShips == i:
                #randomly selects ship orientation
                if random.randint(0, 1):
                    Ships[i].rotate()
                #randomly selects ship place in grid
                if Ships[i].place(random.randint(0, Parameters.N * Parameters.N - 1)):
                    placedShips += 1
                    #checks collision with other ships
                    for y in range(len(Ships)):
                        if y != i and any(j in Ships[i].Positions for j in Ships[y].Positions):
                            Ships[i].reset() 
                            placedShips -= 1
                            break    
            if player is True:
                Ships[i].anchorTo(self.graphics.getPlayerGrid())
            else:        
                Ships[i].anchorTo(self.graphics.getEnemyGrid())
            positions.extend(Ships[i].Positions)
    
    #main game phase
    def playMainGamePhase(self):            
        if self.phase == 0:
            return
        playerAttacks = []  #list of positions attacked by player
        enemyAttacks = []   #list of positions attacked by enemy
        playerHits = 0
        enemyHits = 0
        enemyAttackProbabilities = AttackProbabilityMatrix(Parameters.N, Parameters.N)
        #main game loop
        while self.phase > 0:
            self.graphics.clearScreen()
            self.graphics.drawPlayerGrid()
            self.graphics.drawEnemyGrid()
            for ship in self.Ships:
                self.graphics.drawShip(ship)
            #if game is finished, draw also enemy ships
            if self.phase in (3, 4):
                for ship in self.ShipsEnemy:
                    self.graphics.drawShip(ship)
            for attack in playerAttacks:
                self.graphics.drawHit(True, attack, attack in self.enemyPositions)
            for attack in enemyAttacks:
                self.graphics.drawHit(False, attack, attack in self.playerPositions)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    #mouse clicked after getting game results
                    if self.phase > 2: 
                        self.phase = 0
                    else:
                        #handles an attack by the player
                        attackPos = self.graphics.getAttackPosition()
                        if attackPos >= 0 and attackPos not in playerAttacks:
                            playerAttacks.append(attackPos)
                            if attackPos in self.enemyPositions:
                                playerHits += 1 #enemy ship hit by player
                                if playerHits == len(self.enemyPositions):
                                    self.phase = 3 #player wins
                            if self.phase <= 2:
                                while True:    
                                    #handles an attack by the enemy
                                    attackPos = enemyAttackProbabilities.getNextAttack()
                                    if attackPos not in enemyAttacks: 
                                        enemyAttacks.append(attackPos)
                                        break
                                if attackPos in self.playerPositions:
                                    enemyHits += 1 #player ship hit by enemy
                                    enemyAttackProbabilities.update(attackPos, -1)
                                    if enemyHits == len(self.playerPositions):
                                        self.phase = 4 #enemy wins
                                else: #miss
                                    enemyAttackProbabilities.update(attackPos, 0)
            
            match self.phase:
                case 1 | 2:
                    self.graphics.textWindow(f'{enemyHits} - {playerHits}')
                case 3:
                    self.graphics.textWindow('You win!')
                case 4:
                    self.graphics.textWindow('You lose!')
            self.graphics.updateScreen()
        
if __name__ == '__main__':
    
    game = FleetBattle()
    game.placeShipsPlayer()
    #game.placeShipsRandomly(True)
    game.placeShipsRandomly(False)
    game.playMainGamePhase()
    
    quit()