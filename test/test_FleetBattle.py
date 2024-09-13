import pytest
import src.Parameters as Parameters
from src.FleetBattle import FleetBattle

class MockGraphics:
    def __init__(self):
        True
    def getPlayerGrid(self):
        return (0, 0)
    def getEnemyGrid(self):
        return (0, 0)

@pytest.fixture
def testGame():
    game = FleetBattle(False)
    game.graphics = MockGraphics()
    return game

def testPlaceShipsPlayer(testGame):
    testGame.placeShipsRandomly()
    for pos in testGame.playerPositions:
        assert 0 <= pos < Parameters.N * Parameters.N
    for ship in testGame.Ships:
        assert set(ship.Positions).issubset(set(testGame.playerPositions))
    
def testPlaceShipsEnemy(testGame):
    testGame.placeShipsRandomly(False)
    for pos in testGame.enemyPositions:
        assert 0 <= pos < Parameters.N * Parameters.N
    for ship in testGame.ShipsEnemy:
        assert set(ship.Positions).issubset(set(testGame.enemyPositions))
    
def testPlaceShipsQuit(testGame):
    testGame.phase = 0
    testGame.placeShipsRandomly(True)
    testGame.placeShipsRandomly(False)
    assert len(testGame.playerPositions) == 0
    assert len(testGame.enemyPositions) == 0
    for ship in testGame.Ships:
        assert set(ship.Positions).issubset({-1})
    for ship in testGame.ShipsEnemy:
        assert set(ship.Positions).issubset({-1})