import enum
from random import randint


@enum.unique
class GridObject(enum.Enum):
    EMPTY = enum.auto()
    WALL = enum.auto()
    SNAKE_1 = enum.auto()
    SNAKE_2 = enum.auto()
    APPLE = enum.auto()


class Grid:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.data = [GridObject.EMPTY] * (self.width * self.height)

    def serialize(self):
        assert 0 < self.width
        assert 0 < self.height
        assert self.width < 256
        assert self.height < 256
        return bytes([x.value for x in self.data])

    def deserialize(self, byte_str):
        self.data = list(map(GridObject, byte_str))

    def assert_grid_boundaries(self, row, column):
        assert 0 <= row
        assert 0 <= column
        assert row < self.height
        assert column < self.width

    def element_at(self, row, column):
        self.assert_grid_boundaries(row, column)
        return self.data[row * self.width + column]

    def set_element_at(self, row, column, value):
        self.assert_grid_boundaries(row, column)
        self.data[row * self.width + column] = value

    def __str__(self):
        ret = ""
        for i in range(self.height):
            for j in range(self.width):
                ret += str(self.element_at(i, j).value)
            ret += "\n"
        return ret

    def __getitem__(self, key):
        return self.element_at(*key)

    def __setitem__(self, key, value):
        self.set_element_at(*key, value)


class GridBuilder:
    def __init__(self):
        self.grid = Grid()

    def fill_borders(self):
        for i in range(self.grid.width):
            self.grid.set_element_at(0, i, GridObject.WALL)
            self.grid.set_element_at(self.grid.height - 1, i, GridObject.WALL)
        for i in range(self.grid.height):
            self.grid.set_element_at(i, 0, GridObject.WALL)
            self.grid.set_element_at(i, self.grid.width - 1, GridObject.WALL)

    def reset(self):
        self.grid = Grid()

    def setup_players(self):
        # TODO: Add customizable inital snake length
        player1_snake = [(3, 1), (4, 1), (5, 1)]
        player2_snake = [(6, 8), (5, 8), (4, 8)]

        for pos in player1_snake:
            self.grid[pos] = GridObject.SNAKE_1
        for pos in player2_snake:
            self.grid[pos] = GridObject.SNAKE_2

    def gen_random_apple(self):
        MAX_TRIES = 10
        iter = 0

        # OPTIMIZE: Can lookup only available positions
        while iter < MAX_TRIES:
            xcoord = randint(0, self.grid.width - 1)
            ycoord = randint(0, self.grid.height - 1)
            if self.grid.element_at(xcoord, ycoord) == GridObject.EMPTY:
                self.grid.set_element_at(xcoord, ycoord, GridObject.APPLE)
                return True
            iter += 1

        return False

    def split_grid_half(self):
        for i in range(self.grid.height):
            self.grid.set_element_at(i, self.grid.width // 2, GridObject.WALL)

    def result(self):
        return self.grid
        self.reset()


def __test_serialization():
    a = Grid()
    a.fill_borders()
    a[(2, 2)] = GridObject.SNAKE_1

    b = Grid()
    b.deserialize(a.serialize())

    assert str(a) == str(b)


if __name__ == "__main__":
    gb = GridBuilder()
    gb.setup_players()
    gb.fill_borders()
    gb.split_grid_half()
    gb.gen_random_apple()

    print(gb.result())
