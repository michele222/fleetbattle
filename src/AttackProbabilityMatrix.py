import random

#class handling the probability matrix used to generate the next enemy attack
class AttackProbabilityMatrix:
    
    def __init__(self, sizeX, sizeY):
        self.matrix = [0.1] * sizeX * sizeY #initially all places have the same probability
        self.sizeX = sizeX
        self.sizeY = sizeY
    
    #generates the next position to be attacked
    def getNextAttack(self):
        maxProbability = max(self.matrix)
        #fills array with all positions where probability is currently the highest
        maxProbabilityPositions = [i for i, value in enumerate(self.matrix) if value == maxProbability]
        #returns a random position amongst those with max probability
        return random.choice(maxProbabilityPositions)
    
    #updates the matrix based on previous attack result
    #@position: position of previous attack
    #@result: 0 is a MISS, -1 is a HIT
    def update(self, position, result):
        if position < 0 or position >= self.sizeX * self.sizeY:
            raise ValueError('Invalid position')
        if result not in (0, -1):
            raise ValueError('Invalid result')
        #the previous attack position is updated
        self.matrix[position] = result
        if result < 0: #hit
            positionsToUpdate = []
            if position // self.sizeX > 0:
                positionsToUpdate.append(position - self.sizeX) #up
            if position // self.sizeX < self.sizeY - 1:
                positionsToUpdate.append(position + self.sizeX) #down
            if position % self.sizeX > 0:
                positionsToUpdate.append(position - 1) #left
            if position % self.sizeX < self.sizeX - 1:
                positionsToUpdate.append(position + 1) #right
            #increases the probability for the positions around the hit
            for p in positionsToUpdate:
                if self.matrix[p] > 0:
                    self.matrix[p] += 0.1           