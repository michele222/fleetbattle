import pytest
from src.Ship import Ship
import src.Parameters as Parameters

@pytest.fixture
def testShip():
    return Ship(2)

def testRotationVert(testShip):
    testShip.rotate()
    assert testShip.horizontal is False
    
def testRotationHoriz(testShip):
    testShip.rotate()
    testShip.rotate()
    assert testShip.horizontal is True
    
def testPlace(testShip):
    testShip.place(1)
    assert testShip.Positions[1] == 2
    
def testReset(testShip):
    testShip.place(1)
    testShip.reset()
    assert testShip.Positions[0] == -1
    
def testPlacementOutOfBoundsRight(testShip):
    assert testShip.place(Parameters.N * Parameters.N) is False
    
def testPlacementOutOfBoundsBottom(testShip):
    testShip.rotate()
    assert testShip.place(Parameters.N * Parameters.N) is False
    
def testPlacementBottomRightCornerOut(testShip):
    testShip.rotate()
    assert testShip.place(Parameters.N * Parameters.N - 1) is False
    
def testPlacementBottomRightCornerIn(testShip):
    assert testShip.place(Parameters.N * Parameters.N - 2) is True
    testShip.anchorTo((1, 1))
    assert testShip.body.topleft == (Parameters.SQUARE * (Parameters.N - 2) + 1,
                                     Parameters.SQUARE * (Parameters.N - 1) + 1)