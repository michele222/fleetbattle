import pygame
import random

from src.params import *
from src.Ship import Ship
from src.AttackProbabilityMatrix import AttackProbabilityMatrix

if __name__ == '__main__':
    pygame.init()          

    def drawGrid(offset = (0, 0)): #draw placement grid
        for i in range(N+1):
            pygame.draw.line(screen, (255, 255, 255), (offset[0], offset[1] + i * SQUARE), (offset[0] + N * SQUARE, offset[1] + i * SQUARE))
            pygame.draw.line(screen, (255, 255, 255), (offset[0] + i * SQUARE, offset[1]), (offset[0] + i * SQUARE, offset[1] + N * SQUARE))
        
    def drawHit(offset, pos, hit):
        if hit:
            pygame.draw.rect(screen, (255, 0, 0), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (offset[0] + SQUARE * (pos % N), offset[1] + SQUARE * (pos // N), SQUARE, SQUARE))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    placementGrid = pygame.Rect((0, 0, 2 * MARGIN + N * SQUARE, 2 * MARGIN + N * SQUARE))
    playerGrid = pygame.Rect((MARGIN, MARGIN, N * SQUARE, N * SQUARE))
    attackGrid = pygame.Rect((2 * MARGIN + N * SQUARE, MARGIN, N * SQUARE, N * SQUARE))

    Ships = []
    Ships.append(Ship(1, (MARGIN * 2 + SQUARE * N, MARGIN)))
    Ships.append(Ship(1, (MARGIN * 3 + SQUARE * (N + 1), MARGIN)))
    Ships.append(Ship(1, (MARGIN * 4 + SQUARE * (N + 2), MARGIN)))
    Ships.append(Ship(1, (MARGIN * 5 + SQUARE * (N + 3), MARGIN)))
    Ships.append(Ship(1, (MARGIN * 6 + SQUARE * (N + 4), MARGIN)))
    Ships.append(Ship(2, (MARGIN * 2 + SQUARE * N, MARGIN * 2 + SQUARE)))
    Ships.append(Ship(2, (MARGIN * 3 + SQUARE * (N + 2), MARGIN * 2 + SQUARE)))
    Ships.append(Ship(2, (MARGIN * 4 + SQUARE * (N + 4), MARGIN * 2 + SQUARE)))
    Ships.append(Ship(3, (MARGIN * 2 + SQUARE * N, MARGIN * 3 + SQUARE * 2)))
    Ships.append(Ship(3, (MARGIN * 3 + SQUARE * (N + 3), MARGIN * 3 + SQUARE * 2)))
    Ships.append(Ship(4, (MARGIN * 2 + SQUARE * N, MARGIN * 4 + SQUARE * 3)))
    Ships.append(Ship(4, (MARGIN * 3 + SQUARE * (N + 4), MARGIN * 4 + SQUARE * 3)))
    Ships.append(Ship(5, (MARGIN * 2 + SQUARE * N, MARGIN * 5 + SQUARE * 4)))
    placedShips = 0

    ShipsEnemy = []
    ShipsEnemy.append(Ship(1))
    ShipsEnemy.append(Ship(1))
    ShipsEnemy.append(Ship(1))
    ShipsEnemy.append(Ship(1))
    ShipsEnemy.append(Ship(1))
    ShipsEnemy.append(Ship(2))
    ShipsEnemy.append(Ship(2))
    ShipsEnemy.append(Ship(2))
    ShipsEnemy.append(Ship(2))
    ShipsEnemy.append(Ship(3))
    ShipsEnemy.append(Ship(3))
    ShipsEnemy.append(Ship(4))
    ShipsEnemy.append(Ship(4))
    ShipsEnemy.append(Ship(5))

    playerAttacks = []
    enemyAttacks = []
    playerPositions = []
    enemyPositions = []
    enemyAttackProbabilities = AttackProbabilityMatrix(N, N)
    playerHits = 0
    enemyHits = 0

    holdShip = -1
    phase = 1
    while phase == 1:
    
        screen.fill((0, 0, 0))
    
        drawGrid((MARGIN, MARGIN))
        #drawGrid((MARGIN * 2 + N * SQUARE, MARGIN * 2))
        for ship in Ships: #draw ships
            pygame.draw.rect(screen, (0, 255, 0), ship.body)

        mouseKey = pygame.mouse.get_pressed()
        if mouseKey[0]: #left click mouse
            mousePos = pygame.mouse.get_pos()
            if holdShip < 0: #if no ship is already selected...
                for i in range(len(Ships)):
                    if Ships[i].body.collidepoint(mousePos): #...and i click on a ship...
                        holdShip = i   #...ship is now selected
            if holdShip >= 0:
                Ships[holdShip].body.center = mousePos  #ship follows mouse
        elif holdShip >= 0: #no left click on mouse and ship selected = i just dropped a ship somewhere
            if placementGrid.contains(Ships[holdShip].body):   #is it inside the placement grid (+margins)?
                Ships[holdShip].body.x = round((Ships[holdShip].body.x - MARGIN) / SQUARE) * SQUARE + MARGIN #align to grid
                Ships[holdShip].body.y = round((Ships[holdShip].body.y - MARGIN) / SQUARE) * SQUARE + MARGIN
                if Ships[holdShip].Positions[0] < 0: #i'm moving a ship that was not yet placed
                    placedShips += 1
                gridPosition = (Ships[holdShip].body.x - MARGIN) // SQUARE + (Ships[holdShip].body.y - MARGIN) * N // SQUARE
                Ships[holdShip].place(gridPosition)
                for i in range(len(Ships)):
                    if i != holdShip and any(j in Ships[holdShip].Positions for j in Ships[i].Positions):
                       Ships[holdShip].reset() 
                       placedShips -= 1
                       break           
            else: #dropped ship outside of placement grid
                Ships[holdShip].reset()
            holdShip = -1
        
        if placedShips == len(Ships):
            phase = 2
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase = 0
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and holdShip >= 0: #right mouse button release on a selected ship -> rotate
                Ships[holdShip].rotate()
            
        pygame.display.flip()
    
        clock.tick(60)

    for i in range(len(Ships)):
        playerPositions.extend(Ships[i].Positions)
    placedShips = 0
    for i in range(len(ShipsEnemy)):
        while placedShips == i:    
            if random.randint(0, 1):
                ShipsEnemy[i].rotate()
            if ShipsEnemy[i].place(random.randint(0, N * N - 1)):
                placedShips += 1
                for y in range(len(ShipsEnemy)):
                    if y != i and any(j in ShipsEnemy[i].Positions for j in ShipsEnemy[y].Positions):
                        ShipsEnemy[i].reset() 
                        placedShips -= 1
                        break    
        ShipsEnemy[i].alignTo((MARGIN * 2 + N * SQUARE, MARGIN))
        enemyPositions.extend(ShipsEnemy[i].Positions)

    while phase == 2:
    
        screen.fill((0, 0, 0))
    
        drawGrid((MARGIN, MARGIN))
        drawGrid((MARGIN * 2 + N * SQUARE, MARGIN))
    
        for ship in Ships: #draw ships
            pygame.draw.rect(screen, (0, 255, 0), ship.body)
        # for ship in ShipsEnemy: #draw ships
        #     pygame.draw.rect(screen, (0, 255, 0), ship.body)
        for attack in playerAttacks:
            drawHit(attackGrid.topleft, attack, attack in enemyPositions)
        for attack in enemyAttacks:
            drawHit(playerGrid.topleft, attack, attack in playerPositions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if attackGrid.collidepoint(mousePos):
                    attackPos = (mousePos[0] - attackGrid.x) // SQUARE + ((mousePos[1] - attackGrid.y) // SQUARE) * N
                    if attackPos not in playerAttacks:
                        playerAttacks.append(attackPos)
                        if attackPos in enemyPositions:
                            playerHits += 1
                            if playerHits == len(enemyPositions): #WON
                                phase = 3
                        if phase == 2:
                            while True:    
                                #attackPos = random.randint(0, N * N - 1)
                                attackPos = enemyAttackProbabilities.getNextAttack()
                                if attackPos not in enemyAttacks: 
                                    enemyAttacks.append(attackPos)
                                    break
                            if attackPos in playerPositions: #hit
                                enemyHits += 1
                                enemyAttackProbabilities.update(attackPos, -1)
                                if enemyHits == len(playerPositions): #LOST
                                    phase = 4
                            else: #miss
                                enemyAttackProbabilities.update(attackPos, 0)
    
        pygame.display.flip()
    
        clock.tick(60)
    
    if phase == 3:
        print('Player won')
    elif phase == 4:
        print('Player lost')
    pygame.quit()