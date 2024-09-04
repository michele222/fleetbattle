import random

class AttackProbabilityMatrix:
    
    def __init__(self, sizeX, sizeY):
        self.matrix = [0.1] * sizeX * sizeY
        self.sizeX = sizeX
        self.sizeY = sizeY
        
    def getNextAttack(self):
        maxProbability = max(self.matrix)
        maxProbabilityPositions = [i for i, value in enumerate(self.matrix) if value == maxProbability]
        return random.choice(maxProbabilityPositions)
    
    def update(self, position, result): #result = 0 MISS, -1 HIT
        self.matrix[position] = result
        if result < 0:
            positionsToUpdate = []
            if position // self.sizeX > 0:
                positionsToUpdate.append(position - self.sizeX) #up
            if position // self.sizeX < self.sizeY - 1:
                positionsToUpdate.append(position + self.sizeX) #down
            if position % self.sizeX > 0:
                positionsToUpdate.append(position - 1) #left
            if position % self.sizeX < self.sizeX - 1:
                positionsToUpdate.append(position + 1) #right
            for p in positionsToUpdate:
                if self.matrix[p] > 0:
                    self.matrix[p] += 0.1           