import pygame
import random
from src.Graphics import Graphics

from src.params import *
from src.Ship import Ship
from src.AttackProbabilityMatrix import AttackProbabilityMatrix

class FleetBattle:
    
    def __init__(self):
          
        self.graphics = Graphics()
        
        self.Ships = []
        self.ShipsEnemy = []
        self.playerPositions = []
        self.enemyPositions = []
        self.phase = 1
        
        self.Ships.append(Ship(1, (MARGIN * 2 + SQUARE * N, MARGIN)))
        self.Ships.append(Ship(1, (MARGIN * 3 + SQUARE * (N + 1), MARGIN)))
        self.Ships.append(Ship(1, (MARGIN * 4 + SQUARE * (N + 2), MARGIN)))
        self.Ships.append(Ship(1, (MARGIN * 5 + SQUARE * (N + 3), MARGIN)))
        self.Ships.append(Ship(1, (MARGIN * 6 + SQUARE * (N + 4), MARGIN)))
        self.Ships.append(Ship(2, (MARGIN * 2 + SQUARE * N, MARGIN * 2 + SQUARE)))
        self.Ships.append(Ship(2, (MARGIN * 3 + SQUARE * (N + 2), MARGIN * 2 + SQUARE)))
        self.Ships.append(Ship(2, (MARGIN * 4 + SQUARE * (N + 4), MARGIN * 2 + SQUARE)))
        self.Ships.append(Ship(3, (MARGIN * 2 + SQUARE * N, MARGIN * 3 + SQUARE * 2)))
        self.Ships.append(Ship(3, (MARGIN * 3 + SQUARE * (N + 3), MARGIN * 3 + SQUARE * 2)))
        self.Ships.append(Ship(4, (MARGIN * 2 + SQUARE * N, MARGIN * 4 + SQUARE * 3)))
        self.Ships.append(Ship(4, (MARGIN * 3 + SQUARE * (N + 4), MARGIN * 4 + SQUARE * 3)))
        self.Ships.append(Ship(5, (MARGIN * 2 + SQUARE * N, MARGIN * 5 + SQUARE * 4)))
        
        self.ShipsEnemy.append(Ship(1))
        self.ShipsEnemy.append(Ship(1))
        self.ShipsEnemy.append(Ship(1))
        self.ShipsEnemy.append(Ship(1))
        self.ShipsEnemy.append(Ship(1))
        self.ShipsEnemy.append(Ship(2))
        self.ShipsEnemy.append(Ship(2))
        self.ShipsEnemy.append(Ship(2))
        self.ShipsEnemy.append(Ship(2))
        self.ShipsEnemy.append(Ship(3))
        self.ShipsEnemy.append(Ship(3))
        self.ShipsEnemy.append(Ship(4))
        self.ShipsEnemy.append(Ship(4))
        self.ShipsEnemy.append(Ship(5))

    def placeShipsPlayer(self):
        
        if self.phase == 0:
            return
        placedShips = 0
        holdShip = -1
        while self.phase == 1:
    
            self.graphics.clearScreen()
    
            self.graphics.drawPlayerGrid()
            
            for ship in self.Ships: #draw ships
                self.graphics.drawShip(ship.body)

            mouseKey = pygame.mouse.get_pressed()
            if mouseKey[0]: #left click mouse
                mousePos = pygame.mouse.get_pos()
                if holdShip < 0: #if no ship is already selected...
                    for i in range(len(self.Ships)):
                        if self.Ships[i].body.collidepoint(mousePos): #...and i click on a ship...
                            holdShip = i   #...ship is now selected
                if holdShip >= 0:
                    self.Ships[holdShip].body.center = mousePos  #ship follows mouse
            elif holdShip >= 0: #no left click on mouse and ship selected = i just dropped a ship somewhere
                if self.graphics.isShipInPlacementGrid(self.Ships[holdShip].body):   #is it inside the placement grid (+margins)?
                    self.Ships[holdShip].body = self.graphics.alignToPlacementGrid(self.Ships[holdShip].body) #align to grid
                    if self.Ships[holdShip].Positions[0] < 0: #i'm moving a ship that was not yet placed
                        placedShips += 1
                    gridPosition = self.graphics.getGridPositionFromBody(self.Ships[holdShip].body)
                    self.Ships[holdShip].place(gridPosition)
                    for i in range(len(self.Ships)):
                        if i != holdShip and any(j in self.Ships[holdShip].Positions for j in self.Ships[i].Positions):
                           self.Ships[holdShip].reset() 
                           placedShips -= 1
                           break           
                else: #dropped ship outside of placement grid
                    self.Ships[holdShip].reset()
                holdShip = -1
        
            if placedShips == len(self.Ships):
                self.phase = 2
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and holdShip >= 0: #right mouse button release on a selected ship -> rotate
                    self.Ships[holdShip].rotate()
            
            self.graphics.updateScreen()
    
            self.graphics.clock.tick(60)

        for i in range(len(self.Ships)):
            self.playerPositions.extend(self.Ships[i].Positions)
            
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
                if random.randint(0, 1):
                    Ships[i].rotate()
                if Ships[i].place(random.randint(0, N * N - 1)):
                    placedShips += 1
                    for y in range(len(Ships)):
                        if y != i and any(j in Ships[i].Positions for j in Ships[y].Positions):
                            Ships[i].reset() 
                            placedShips -= 1
                            break    
            if player is True:
                Ships[i].alignTo((MARGIN, MARGIN))
            else:        
                Ships[i].alignTo((MARGIN * 2 + N * SQUARE, MARGIN))
            positions.extend(Ships[i].Positions)

    def playMainGamePhase(self):            
        
        if self.phase == 0:
            return
        playerAttacks = []
        enemyAttacks = []
        playerHits = 0
        enemyHits = 0
        enemyAttackProbabilities = AttackProbabilityMatrix(N, N)
        while self.phase > 0:
    
            self.graphics.clearScreen()
            self.graphics.drawPlayerGrid()
            self.graphics.drawEnemyGrid()
    
            for ship in self.Ships: #draw ships
                self.graphics.drawShip(ship.body)
            if self.phase == 4:
                for ship in self.ShipsEnemy: #draw also enemy ships if game is lost
                    self.graphics.drawShip(ship.body)

            for attack in playerAttacks:
                self.graphics.drawHit(True, attack, attack in self.enemyPositions)
            for attack in enemyAttacks:
                self.graphics.drawHit(False, attack, attack in self.playerPositions)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.phase > 2:
                        self.phase = 0
                    else:
                        mousePos = pygame.mouse.get_pos()
                        if self.graphics.playerAttacked(mousePos):
                            attackPos = self.graphics.getAttackPosition(mousePos)
                            if attackPos not in playerAttacks:
                                playerAttacks.append(attackPos)
                                if attackPos in self.enemyPositions:
                                    playerHits += 1
                                    if playerHits == len(self.enemyPositions): #WON
                                        self.phase = 3
                                if self.phase <= 2:
                                    while True:    
                                        attackPos = enemyAttackProbabilities.getNextAttack()
                                        if attackPos not in enemyAttacks: 
                                            enemyAttacks.append(attackPos)
                                            break
                                    if attackPos in self.playerPositions: #hit
                                        enemyHits += 1
                                        enemyAttackProbabilities.update(attackPos, -1)
                                        if enemyHits == len(self.playerPositions): #LOST
                                            self.phase = 4
                                    else: #miss
                                        enemyAttackProbabilities.update(attackPos, 0)
            
            if self.phase == 3:
                self.graphics.textWindow('You win!')
            elif self.phase == 4:
                self.graphics.textWindow('You lose!')

            self.graphics.updateScreen()
    
            #self.graphics.clock.tick(60)
        
if __name__ == '__main__':
    
    game = FleetBattle()
    #game.placeShipsPlayer()
    game.placeShipsRandomly(True)
    game.placeShipsRandomly(False)
    game.playMainGamePhase()
    
    quit()