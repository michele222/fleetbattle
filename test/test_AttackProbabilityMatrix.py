import pytest
from src.AttackProbabilityMatrix import AttackProbabilityMatrix

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