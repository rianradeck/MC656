import pytest

from common.grid import Grid, GridObject


def test_serialize():
    grid_a = Grid()
    grid_a.fill_borders()
    grid_b = Grid()

    grid_b.deserialize(grid_a.serialize())
    assert str(grid_a) == str(grid_b)


def test_grid():
    grid = Grid()

    grid.set_element_at(0, 0, GridObject.APPLE)

    assert grid.element_at(0, 0) == GridObject.APPLE

    with pytest.raises(AssertionError):
        grid.set_element_at(grid.height, grid.width, GridObject.APPLE)
