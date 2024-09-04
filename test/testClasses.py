from pickle import FALSE
import pytest
from src.Ship import Ship
import src.FleetBattle

def testAddShip():
    testShip = Ship(2)
    testShip.rotate()
    assert testShip.horizontal is False
    testShip.rotate()
    assert testShip.horizontal is True

def testRemoveShip():
    pass