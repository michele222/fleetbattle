import pytest
import src.parameters as parameters
from src.fleet_battle import FleetBattle

class MockGraphics:
    def __init__(self):
        pass
    def get_player_grid(self):
        return 0, 0
    def get_enemy_grid(self):
        return 0, 0

@pytest.fixture
def test_game():
    game = FleetBattle(False)
    game.graphics = MockGraphics()
    return game

def test_place_ships_player(test_game):
    test_game.place_ships_randomly()
    for pos in test_game.player_positions:
        assert 0 <= pos < parameters.N * parameters.N
    for ship in test_game.ships:
        assert set(ship.positions).issubset(set(test_game.player_positions))
    
def test_place_ships_enemy(test_game):
    test_game.place_ships_randomly(False)
    for pos in test_game.enemy_positions:
        assert 0 <= pos < parameters.N * parameters.N
    for ship in test_game.ships_enemy:
        assert set(ship.positions).issubset(set(test_game.enemy_positions))
    
def test_place_ships_quit(test_game):
    test_game.phase = 0
    test_game.place_ships_randomly(True)
    test_game.place_ships_randomly(False)
    assert len(test_game.player_positions) == 0
    assert len(test_game.enemy_positions) == 0
    for ship in test_game.ships:
        assert set(ship.positions).issubset({-1})
    for ship in test_game.ships_enemy:
        assert set(ship.positions).issubset({-1})