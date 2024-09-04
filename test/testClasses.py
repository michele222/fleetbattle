import pytest
from src.Ship import Ship
from src.AttackProbabilityMatrix import AttackProbabilityMatrix
import src.FleetBattle
from src.params import *

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
    assert testShip.place(N*N) is False
    
def testPlacementOutOfBoundsBottom(testShip):
    testShip.rotate()
    assert testShip.place(N*N) is False
    
def testPlacementBottomRightCornerOut(testShip):
    testShip.rotate()
    assert testShip.place(N*N - 1) is False
    
def testPlacementBottomRightCornerIn(testShip):
    assert testShip.place(N*N - 2) is True
    
def testAttackProbabilityMatrix():
    testMatrix = AttackProbabilityMatrix(5, 5)
    testMatrix.update(0, 0)
    assert testMatrix.getNextAttack() != 0
    testMatrix.update(1, -1)
    testMatrix.update(2, 0)
    assert testMatrix.getNextAttack() == 6
    with pytest.raises(ValueError):
        testMatrix.update(-1, 0)
    with pytest.raises(ValueError):
        testMatrix.update(25, 0)
    with pytest.raises(ValueError):
        testMatrix.update(1, 2)