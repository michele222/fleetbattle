import pygame
import random

from src.params import *
from src.Ship import Ship
from src.AttackProbabilityMatrix import AttackProbabilityMatrix

class FleetBattle:
    
    def __init__(self):
          
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.Ships = []
        self.ShipsEnemy = []
        self.playerPositions = []
        self.enemyPositions = []
        self.holdShip = -1
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

    def drawGrid(self, offset = (0, 0)): #draw placement grid
        for i in range(N+1):
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0], offset[1] + i * SQUARE), (offset[0] + N * SQUARE, offset[1] + i * SQUARE))
            pygame.draw.line(self.screen, (255, 255, 255), (offset[0] + i * SQUARE, offset[1]), (offset[0] + i * SQUARE, offset[1] + N * SQUARE))
        
    def drawHit(self, offset, pos, hit):
        if hit:
            pygame.draw.rect(self.screen, (255, 0, 0), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))

    def shipPlacementPhasePlayer(self):
        placementGrid = pygame.Rect((0, 0, 2 * MARGIN + N * SQUARE, 2 * MARGIN + N * SQUARE))
        placedShips = 0
        while self.phase == 1:
    
            self.screen.fill((0, 0, 0))
    
            self.drawGrid((MARGIN, MARGIN))
            
            for ship in self.Ships: #draw ships
                pygame.draw.rect(self.screen, (0, 255, 0), ship.body)

            mouseKey = pygame.mouse.get_pressed()
            if mouseKey[0]: #left click mouse
                mousePos = pygame.mouse.get_pos()
                if self.holdShip < 0: #if no ship is already selected...
                    for i in range(len(self.Ships)):
                        if self.Ships[i].body.collidepoint(mousePos): #...and i click on a ship...
                            self.holdShip = i   #...ship is now selected
                if self.holdShip >= 0:
                    self.Ships[self.holdShip].body.center = mousePos  #ship follows mouse
            elif self.holdShip >= 0: #no left click on mouse and ship selected = i just dropped a ship somewhere
                if placementGrid.contains(self.Ships[self.holdShip].body):   #is it inside the placement grid (+margins)?
                    self.Ships[self.holdShip].body.x = round((self.Ships[self.holdShip].body.x - MARGIN) / SQUARE) * SQUARE + MARGIN #align to grid
                    self.Ships[self.holdShip].body.y = round((self.Ships[self.holdShip].body.y - MARGIN) / SQUARE) * SQUARE + MARGIN
                    if self.Ships[self.holdShip].Positions[0] < 0: #i'm moving a ship that was not yet placed
                        placedShips += 1
                    gridPosition = (self.Ships[self.holdShip].body.x - MARGIN) // SQUARE + (self.Ships[self.holdShip].body.y - MARGIN) * N // SQUARE
                    self.Ships[self.holdShip].place(gridPosition)
                    for i in range(len(self.Ships)):
                        if i != self.holdShip and any(j in self.Ships[self.holdShip].Positions for j in self.Ships[i].Positions):
                           self.Ships[self.holdShip].reset() 
                           placedShips -= 1
                           break           
                else: #dropped ship outside of placement grid
                    self.Ships[self.holdShip].reset()
                self.holdShip = -1
        
            if placedShips == len(self.Ships):
                self.phase = 2
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and self.holdShip >= 0: #right mouse button release on a selected ship -> rotate
                    self.Ships[self.holdShip].rotate()
            
            pygame.display.flip()
    
            self.clock.tick(60)

        for i in range(len(self.Ships)):
            self.playerPositions.extend(self.Ships[i].Positions)
            
    def shipPlacementPhaseEnemy(self):
        placedShips = 0
        for i in range(len(self.ShipsEnemy)):
            while placedShips == i:    
                if random.randint(0, 1):
                    self.ShipsEnemy[i].rotate()
                if self.ShipsEnemy[i].place(random.randint(0, N * N - 1)):
                    placedShips += 1
                    for y in range(len(self.ShipsEnemy)):
                        if y != i and any(j in self.ShipsEnemy[i].Positions for j in self.ShipsEnemy[y].Positions):
                            self.ShipsEnemy[i].reset() 
                            placedShips -= 1
                            break    
            self.ShipsEnemy[i].alignTo((MARGIN * 2 + N * SQUARE, MARGIN))
            self.enemyPositions.extend(self.ShipsEnemy[i].Positions)

    def playMainGamePhase(self):            
        playerGrid = pygame.Rect((MARGIN, MARGIN, N * SQUARE, N * SQUARE))
        attackGrid = pygame.Rect((2 * MARGIN + N * SQUARE, MARGIN, N * SQUARE, N * SQUARE))
        playerAttacks = []
        enemyAttacks = []
        playerHits = 0
        enemyHits = 0
        enemyAttackProbabilities = AttackProbabilityMatrix(N, N)
        while self.phase == 2:
    
            self.screen.fill((0, 0, 0))
    
            self.drawGrid((MARGIN, MARGIN))
            self.drawGrid((MARGIN * 2 + N * SQUARE, MARGIN))
    
            for ship in self.Ships: #draw ships
                pygame.draw.rect(self.screen, (0, 255, 0), ship.body)

            for attack in playerAttacks:
                self.drawHit(attackGrid.topleft, attack, attack in self.enemyPositions)
            for attack in enemyAttacks:
                self.drawHit(playerGrid.topleft, attack, attack in self.playerPositions)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousePos = pygame.mouse.get_pos()
                    if attackGrid.collidepoint(mousePos):
                        attackPos = (mousePos[0] - attackGrid.x) // SQUARE + ((mousePos[1] - attackGrid.y) // SQUARE) * N
                        if attackPos not in playerAttacks:
                            playerAttacks.append(attackPos)
                            if attackPos in self.enemyPositions:
                                playerHits += 1
                                if playerHits == len(self.enemyPositions): #WON
                                    self.phase = 3
                            if self.phase == 2:
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
    
            pygame.display.flip()
    
            self.clock.tick(60)
    
    def resultPhase(self):
        if self.phase == 3:
            print('Player won')
        elif self.phase == 4:
            print('Player lost')
        
if __name__ == '__main__':
    pygame.init()  
    
    game = FleetBattle()
    game.shipPlacementPhasePlayer()
    game.shipPlacementPhaseEnemy()
    game.playMainGamePhase()
    game.resultPhase()
    
    pygame.quit()