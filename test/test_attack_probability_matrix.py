import pytest
from src.attack_probability_matrix import AttackProbabilityMatrix

def test_attack_probability_matrix():
    test_matrix = AttackProbabilityMatrix(5, 5)
    test_matrix.update((0, 0), 0)
    assert test_matrix.get_next_attack() != (0, 0)
    test_matrix.update((1, 0), -1)
    test_matrix.update((2, 0), 0)
    assert test_matrix.get_next_attack() == (1, 1)
    with pytest.raises(ValueError):
        test_matrix.update((-1, 0), 0)
    with pytest.raises(ValueError):
        test_matrix.update((0, -1), 0)
    with pytest.raises(ValueError):
        test_matrix.update((5, 0), 0)
    with pytest.raises(ValueError):
        test_matrix.update((4, 5), 0)
    with pytest.raises(ValueError):
        test_matrix.update((1, 1), 2)