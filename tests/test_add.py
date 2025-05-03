import pytest
from app.calculations import add

@pytest.mark.parametrize("num1, num2, expected", 
                        [
    (1, 2, 3),
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(num1, num2, expected):
    print("Running test_add")
    assert add(num1, num2) == expected