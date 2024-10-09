import pytest
from src.attack_probability_matrix import AttackProbabilityMatrix

def test_attack_probability_matrix():
    test_matrix = AttackProbabilityMatrix(5, 5)
    test_matrix.update(0, 0)
    assert test_matrix.get_next_attack() != 0
    test_matrix.update(1, -1)
    test_matrix.update(2, 0)
    assert test_matrix.get_next_attack() == 6
    with pytest.raises(ValueError):
        test_matrix.update(-1, 0)
    with pytest.raises(ValueError):
        test_matrix.update(25, 0)
    with pytest.raises(ValueError):
        test_matrix.update(1, 2)