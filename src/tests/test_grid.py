import pytest

from common.grid import Grid, GridBuilder, GridObject


def all_empty():
    grid = Grid()
    for i in range(grid.height):
        for j in range(grid.width):
            if grid.element_at(i, j) != GridObject.EMPTY:
                return False
    return True


def test_serialize():
    gb = GridBuilder()
    gb.fill_borders()
    grid_a = gb.result()
    grid_b = Grid()

    grid_b.deserialize(grid_a.serialize())
    assert str(grid_a) == str(grid_b)


def test_grid():
    grid = Grid()

    grid.set_element_at(0, 0, GridObject.APPLE)

    assert grid.element_at(0, 0) == GridObject.APPLE

    with pytest.raises(AssertionError):
        grid.set_element_at(grid.height, grid.width, GridObject.APPLE)


def test_grid_limits():
    grid = Grid()

    for i in range(grid.height):
        with pytest.raises(AssertionError):
            grid.set_element_at(i, -1, GridObject.SNAKE_1)
        grid.set_element_at(i, 0, GridObject.SNAKE_1)
        assert grid.element_at(i, 0) == GridObject.SNAKE_1
        grid.set_element_at(i, 0, GridObject.EMPTY)

    for j in range(grid.width):
        with pytest.raises(AssertionError):
            grid.set_element_at(-1, j, GridObject.SNAKE_1)
        grid.set_element_at(0, j, GridObject.SNAKE_1)
        assert grid.element_at(0, j) == GridObject.SNAKE_1
        grid.set_element_at(i, 0, GridObject.EMPTY)

    assert all_empty()
