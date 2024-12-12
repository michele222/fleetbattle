import pygame
import random

from src import parameters
from src.graphics import Graphics
from src.ship import Ship
from src.attack_probability_matrix import AttackProbabilityMatrix

#main class running the game
class FleetBattle:
    
    #game initialization
    #@graphics: True initializes graphics as well. False is used for testing
    def __init__(self, graphics = True):
        self.ships = []             #player ships
        self.ships_enemy = []        #enemy ships
        self.player_positions = []   #positions occupied by player ships
        self.enemy_positions = []    #positions occupied by enemy ships
        self.phase = 1              #game phase
        if graphics:
            self.graphics = Graphics()
        for i in parameters.SHIPS:
            self.ships_enemy.append(Ship(i))
            if graphics:
                self.ships.append(Ship(i, self.graphics.get_space_for_ship_size(i)))
            else:
                self.ships.append(Ship(i))    

    #manual placement of ships by player
    def place_ships_player(self):
        if self.phase == 0:
            return
        placed_ships = 0
        hold_ship = -1 #no ship selected: -1, ship selected: ship id
        #ship placement phase
        while self.phase == 1:
            self.graphics.clear_screen()
            self.graphics.draw_player_grid()
            self.graphics.text_window('Place the ships in the grid. Right click to rotate.')
            for ship in self.ships:
                self.graphics.draw_ship(ship)

            mouse_key = pygame.mouse.get_pressed()
            if mouse_key[0]: #left click
                mouse_pos = pygame.mouse.get_pos()
                #ship is selected with mouse
                if hold_ship < 0:
                    for i in range(len(self.ships)):
                        if self.ships[i].body.collidepoint(mouse_pos):
                            hold_ship = i
                #selected ship follows mouse
                if hold_ship >= 0:
                    self.ships[hold_ship].body.center = mouse_pos
            #selected ship has been released by mouse
            elif hold_ship >= 0:
                #selected ship has been released inside the placement area
                if self.graphics.is_ship_in_placement_area(self.ships[hold_ship].body):
                    self.ships[hold_ship].body = self.graphics.align_to_player_grid(self.ships[hold_ship].body)
                    #this is a ship not placed before
                    if not self.ships[hold_ship].positions[0]:
                        placed_ships += 1
                    grid_position = self.graphics.get_grid_position_from_body(self.ships[hold_ship].body)
                    self.ships[hold_ship].place(grid_position)
                    #check collisions with other ships
                    for i in range(len(self.ships)):
                        #in case of collision, the ship is placed back in its default position outside the grid
                        if i != hold_ship and any(j in self.ships[hold_ship].positions for j in self.ships[i].positions):
                           self.ships[hold_ship].reset() 
                           placed_ships -= 1
                           break           
                else: #ship released outside of placement grid
                    #this is a ship that was previously placed
                    if self.ships[hold_ship].positions[0]:
                        placed_ships -= 1
                    self.ships[hold_ship].reset()
                hold_ship = -1
            
            #all ships are placed
            if placed_ships == len(self.ships):
                self.phase = 2
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                #right mouse button release on a selected ship rotates the ship
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and hold_ship >= 0:
                    self.ships[hold_ship].rotate()
            
            self.graphics.update_screen()
            self.graphics.clock.tick(60)

        for i in range(len(self.ships)):
            self.player_positions.extend(self.ships[i].positions)
    
    #random placement of ships in grid
    #@player: defines whether player or enemy ships are randomly placed
    def place_ships_randomly(self, player = True):
        if self.phase == 0:
            return
        placed_ships = 0
        if player is True:
            ships = self.ships
            positions = self.player_positions
        else:
            ships = self.ships_enemy    
            positions = self.enemy_positions
        for i in range(len(ships)):
            while placed_ships == i:
                #randomly selects ship orientation
                if random.randint(0, 1):
                    ships[i].rotate()
                #randomly selects ship place in grid
                if ships[i].place((random.randrange(0, parameters.N[0]),
                                   random.randrange(0, parameters.N[1]))):
                    placed_ships += 1
                    #checks collision with other ships
                    for j in range(len(ships)):
                        if j != i and any(pos in ships[i].positions for pos in ships[j].positions):
                            ships[i].reset() 
                            placed_ships -= 1
                            break    
            if player is True:
                ships[i].anchor_to(self.graphics.get_player_grid())
            else:        
                ships[i].anchor_to(self.graphics.get_enemy_grid())
            positions.extend(ships[i].positions)
    
    #main game phase
    def play_main_game_phase(self):            
        if self.phase == 0:
            return
        player_attacks = []  #list of positions attacked by player
        enemy_attacks = []   #list of positions attacked by enemy
        player_hits = 0
        enemy_hits = 0
        enemy_attack_probabilities = AttackProbabilityMatrix(parameters.N[0], parameters.N[1])
        #main game loop
        while self.phase > 0:
            self.graphics.clear_screen()
            self.graphics.draw_player_grid()
            self.graphics.draw_enemy_grid()
            for ship in self.ships:
                self.graphics.draw_ship(ship)
            #if game is finished, draw also enemy ships
            if self.phase in (3, 4):
                for ship in self.ships_enemy:
                    self.graphics.draw_ship(ship)
            for attack in player_attacks:
                self.graphics.draw_hit(True, attack, attack in self.enemy_positions)
            for attack in enemy_attacks:
                self.graphics.draw_hit(False, attack, attack in self.player_positions)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.phase = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    #mouse clicked after getting game results
                    if self.phase > 2: 
                        self.phase = 0
                    else:
                        #handles an attack by the player
                        attack_pos = self.graphics.get_attack_position()
                        if len(attack_pos) > 0 and attack_pos not in player_attacks:
                            player_attacks.append(attack_pos)
                            if attack_pos in self.enemy_positions:
                                player_hits += 1 #enemy ship hit by player
                                if player_hits == len(self.enemy_positions):
                                    self.phase = 3 #player wins
                            if self.phase <= 2:
                                while True:    
                                    #handles an attack by the enemy
                                    attack_pos = enemy_attack_probabilities.get_next_attack()
                                    if attack_pos not in enemy_attacks: 
                                        enemy_attacks.append(attack_pos)
                                        break
                                if attack_pos in self.player_positions:
                                    enemy_hits += 1 #player ship hit by enemy
                                    enemy_attack_probabilities.update(attack_pos, -1)
                                    if enemy_hits == len(self.player_positions):
                                        self.phase = 4 #enemy wins
                                else: #miss
                                    enemy_attack_probabilities.update(attack_pos, 0)
            
            match self.phase:
                case 1 | 2:
                    self.graphics.text_window(f'{enemy_hits} - {player_hits}')
                case 3:
                    self.graphics.text_window('You win!')
                case 4:
                    self.graphics.text_window('You lose!')
            self.graphics.update_screen()
