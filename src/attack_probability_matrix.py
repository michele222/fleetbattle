import random

#class handling the probability matrix used to generate the next enemy attack
class AttackProbabilityMatrix:
    
    def __init__(self, size_x, size_y):
        self.matrix = [0.1] * size_x * size_y #initially all places have the same probability
        self.size_x = size_x
        self.size_y = size_y
    
    #generates the next position to be attacked
    def get_next_attack(self):
        max_probability = max(self.matrix)
        #fills array with all positions where probability is currently the highest
        max_probability_positions = [i for i, value in enumerate(self.matrix) if value == max_probability]
        #returns a random position amongst those with max probability
        return random.choice(max_probability_positions)
    
    #updates the matrix based on previous attack result
    #@position: position of previous attack
    #@result: 0 is a MISS, -1 is a HIT
    def update(self, position, result):
        if position < 0 or position >= self.size_x * self.size_y:
            raise ValueError('Invalid position')
        if result not in (0, -1):
            raise ValueError('Invalid result')
        #the previous attack position is updated
        self.matrix[position] = result
        if result < 0: #hit
            positions_to_update = []
            if position // self.size_x > 0:
                positions_to_update.append(position - self.size_x) #up
            if position // self.size_x < self.size_y - 1:
                positions_to_update.append(position + self.size_x) #down
            if position % self.size_x > 0:
                positions_to_update.append(position - 1) #left
            if position % self.size_x < self.size_x - 1:
                positions_to_update.append(position + 1) #right
            #increases the probability for the positions around the hit
            for p in positions_to_update:
                if self.matrix[p] > 0:
                    self.matrix[p] += 0.1           