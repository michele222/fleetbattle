import pytest
from src.ship import Ship
import src.parameters as parameters

@pytest.fixture
def test_ship():
    return Ship(2)

def test_rotation_vertical(test_ship):
    test_ship.rotate()
    assert test_ship.horizontal is False
    
def test_rotation_horizontal(test_ship):
    test_ship.rotate()
    test_ship.rotate()
    assert test_ship.horizontal is True
    
def test_place(test_ship):
    test_ship.place((1, 0))
    assert test_ship.positions[1] == (2, 0)
    
def test_reset(test_ship):
    test_ship.place((1, 0))
    test_ship.reset()
    assert test_ship.positions[0] is None

def test_placement_out_of_bounds_right(test_ship):
    assert test_ship.place((parameters.N[0], parameters.N[1])) is False
    
def test_placement_out_of_bounds_bottom(test_ship):
    test_ship.rotate()
    assert test_ship.place((parameters.N[0], parameters.N[1])) is False
    
def test_placement_bottom_right_corner_out(test_ship):
    test_ship.rotate()
    assert test_ship.place((parameters.N[0] - 1, parameters.N[1] - 1)) is False
    
def test_placement_bottom_right_corner_in(test_ship):
    assert test_ship.place((parameters.N[0] - 2, parameters.N[1] - 1)) is True
    test_ship.anchor_to((1, 1))
    assert test_ship.body.topleft == (parameters.SQUARE * (parameters.N[0] - 2) + 1,
                                      parameters.SQUARE * (parameters.N[1] - 1) + 1)