from pathlib import Path

import pygame

from src import parameters


# class handling all graphic elements of the game
class Graphics:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((parameters.WIDTH, parameters.HEIGHT))
        pygame.display.set_caption('FleetBattle')
        self.clock = pygame.time.Clock()
        # the grid showing player ships
        self.player_grid = pygame.Rect((parameters.MARGIN,
                                        parameters.MARGIN,
                                        parameters.N[0] * parameters.SQUARE,
                                        parameters.N[1] * parameters.SQUARE))
        # the grid showing player attacks
        self.attack_grid = pygame.Rect((2 * parameters.MARGIN + parameters.N[0] * parameters.SQUARE,
                                        parameters.MARGIN,
                                        parameters.N[0] * parameters.SQUARE,
                                        parameters.N[1] * parameters.SQUARE))
        # the area where ships are placed by the player. Equals the playerGrid with margin around
        self.placement_area = pygame.Rect((self.player_grid.topleft[0] - parameters.MARGIN,
                                           self.player_grid.topleft[1] - parameters.MARGIN,
                                           parameters.N[0] * parameters.SQUARE + 2 * parameters.MARGIN,
                                           parameters.N[1] * parameters.SQUARE + 2 * parameters.MARGIN))
        # before placement, ships are initially drawn in an invisible grid starting with position placementPos
        self.placement_pos = (0, 0)
        # background image
        path_to_images = Path(__file__).parent.parent.joinpath('assets')
        self.bg_texture = pygame.image.load(path_to_images.joinpath('bg.png')).convert_alpha()
        self.bg_texture = pygame.transform.smoothscale(self.bg_texture,
                                                       (parameters.N[0] * parameters.SQUARE,
                                                        parameters.N[1] * parameters.SQUARE))
        # ship images are initialized based on ship length
        self.ship_textures = {}
        for i in range(1, 6):
            self.ship_textures[i] = pygame.image.load(path_to_images.joinpath(f'ship{i}.png')).convert_alpha()
            self.ship_textures[i] = pygame.transform.smoothscale(self.ship_textures[i],
                                                                 (i * parameters.SQUARE,
                                                                  parameters.SQUARE))
        # explosion images
        self.hit_texture = {
            True: pygame.image.load(path_to_images.joinpath('explosion.png')).convert_alpha(),
            # True: explosion on ship (hit)
            False: pygame.image.load(path_to_images.joinpath('explosion_sea.png')).convert_alpha()
            # False: explosion at sea (miss)
        }
        for i in self.hit_texture:
            self.hit_texture[i] = pygame.transform.smoothscale(self.hit_texture[i],
                                                               (parameters.SQUARE,
                                                                parameters.SQUARE))

    def __del__(self):
        pygame.quit()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    # draws all objects on screen
    def update_screen(self):
        pygame.display.flip()

    # draws an N*N grid with background image
    # @offset: top left point of the grid
    def draw_grid(self, offset=(0, 0)):
        self.screen.blit(self.bg_texture, offset)
        for i in range(parameters.N[0] + 1):
            # vertical lines
            pygame.draw.line(self.screen,
                             (255, 255, 255),
                             (offset[0] + i * parameters.SQUARE,
                              offset[1]),
                             (offset[0] + i * parameters.SQUARE,
                              offset[1] + parameters.N[1] * parameters.SQUARE))
        for i in range(parameters.N[1] + 1):
            # horizontal lines
            pygame.draw.line(self.screen,
                             (255, 255, 255),
                             (offset[0],
                              offset[1] + i * parameters.SQUARE),
                             (offset[0] + parameters.N[0] * parameters.SQUARE,
                              offset[1] + i * parameters.SQUARE))

    def draw_player_grid(self):
        self.draw_grid(self.player_grid.topleft)

    def draw_enemy_grid(self):
        self.draw_grid(self.attack_grid.topleft)

    # draws a hit image (explosion)
    # @isPlayer: True when player attacks, False when enemy attacks
    # @pos: position of the attack on grid
    # @hit: True when hit, False when miss
    def draw_hit(self, is_player, pos, hit):
        offset = self.player_grid.topleft
        if is_player:
            offset = self.attack_grid.topleft
        self.screen.blit(self.hit_texture[hit],
                         (offset[0] + parameters.SQUARE * pos[0],
                          offset[1] + parameters.SQUARE * pos[1]))

    # draws a ship image
    # @ship: object ship
    def draw_ship(self, ship):
        if ship.horizontal:
            self.screen.blit(self.ship_textures[ship.length],
                             ship.body.topleft)
        else:
            self.screen.blit(pygame.transform.rotate(self.ship_textures[ship.length],
                                                     -90),
                             ship.body.topleft)

    # gets attack position based on mouse position
    # return: position in attack grid, () if outside grid
    def get_attack_position(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.attack_grid.collidepoint(mouse_pos):
            return ((mouse_pos[0] - self.attack_grid.x) // parameters.SQUARE,
                    (mouse_pos[1] - self.attack_grid.y) // parameters.SQUARE)
        else:
            return ()

    # gets grid position from ship rectangle
    # @body: ship body rectangle
    # return: grid position
    def get_grid_position_from_body(self, body):
        return ((body.x - self.player_grid.left) // parameters.SQUARE,
                (body.y - self.player_grid.top) // parameters.SQUARE)

    # checks whether a ship rectangle is fully in the placement area
    # @body: ship body rectangle
    def is_ship_in_placement_area(self, body):
        return self.placement_area.contains(body)

    # aligns a ship rectangle to the placement grid
    # @body: ship body rectangle
    # return: aligned ship body rectangle
    def align_to_player_grid(self, body):
        body.x = round((body.x - self.player_grid.left) / parameters.SQUARE) * parameters.SQUARE + self.player_grid.left
        body.y = round((body.y - self.player_grid.top) / parameters.SQUARE) * parameters.SQUARE + self.player_grid.top
        return body

    def get_player_grid(self):
        return self.player_grid.topleft

    def get_enemy_grid(self):
        return self.attack_grid.topleft

    # assigns the next available spot for a ship for the initial ship drawing phase
    # ships are drawn in the attack grid with extra margins, the grid itself is not drawn in this phase
    # @size: size of the ship to be placed
    # return: next available position (x, y) that can fit the ship
    def get_space_for_ship_size(self, size):
        # if the ship doesn't fit in the current line, move to the leftmost position one line down
        if self.placement_pos[0] + size > parameters.N[0]:
            self.placement_pos = (0, self.placement_pos[1] + 1)
        ret = (self.attack_grid.topleft[0] + self.placement_pos[0] * parameters.SQUARE,
               self.attack_grid.topleft[1] + self.placement_pos[1] * (parameters.SQUARE + parameters.MARGIN))
        self.placement_pos = (self.placement_pos[0] + size + 1, self.placement_pos[1])
        return ret

    # displays a message in the center of the screen, below the grids
    # @message: the message to be displayed
    def text_window(self, message):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.midtop = (parameters.WIDTH // 2,
                            self.player_grid.bottomright[0] + parameters.MARGIN // 2)
        self.screen.blit(text, text_rect)
