import random


# class handling the probability matrix used to generate the next enemy attack
class AttackProbabilityMatrix:

    def __init__(self, size_x, size_y):
        self.matrix = [[0.1] * size_y for _ in range(size_x)]  # initially all places have the same probability
        self.size = (size_x, size_y)

    # generates the next position to be attacked
    def get_next_attack(self):
        max_probability = max(max(row) for row in self.matrix)
        # fills array with all positions where probability is currently the highest
        max_probability_positions = [(x, y) for x, row in enumerate(self.matrix) for y, value in enumerate(row) if
                                     value == max_probability]
        # returns a random position amongst those with max probability
        return random.choice(max_probability_positions)

    # updates the matrix based on previous attack result
    # @position: position of previous attack
    # @result: 0 is a MISS, -1 is a HIT
    def update(self, position, result):
        if not position:
            raise ValueError('Invalid position')
        if position[0] < 0 or position[1] < 0:
            raise ValueError('Invalid position')
        if position[0] >= self.size[0] or position[1] >= self.size[1]:
            raise ValueError('Invalid position')
        if result not in (0, -1):
            raise ValueError('Invalid result')
        # the previous attack position is updated
        self.matrix[position[0]][position[1]] = result
        if result < 0:  # hit
            positions_to_update = []
            if position[0] > 0:
                positions_to_update.append((position[0] - 1, position[1]))  # left
            if position[0] < self.size[0] - 1:
                positions_to_update.append((position[0] + 1, position[1]))  # right
            if position[1] > 0:
                positions_to_update.append((position[0], position[1] - 1))  # up
            if position[1] < self.size[1] - 1:
                positions_to_update.append((position[0], position[1] + 1))  # down
            # increases the probability for the positions around the hit
            for p in positions_to_update:
                if self.matrix[p[0]][p[1]] > 0:
                    self.matrix[p[0]][p[1]] += 0.1
