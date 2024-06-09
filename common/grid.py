import enum


@enum.unique
class GridObject(enum.Enum):
    EMPTY = enum.auto()
    WALL = enum.auto()
    APPLE = enum.auto()
    SNAKE_1 = enum.auto()
    SNAKE_2 = enum.auto()

    def snake_from_index(idx):
        return GridObject(GridObject.SNAKE_1.value + idx)


class Grid:
    def __init__(self):
        self.width = 15
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

    def element_at(self, row, column):
        assert 0 <= row
        assert 0 <= column
        assert row < self.height
        assert column < self.width
        return self.data[row * self.width + column]

    def set_element_at(self, row, column, value):
        assert 0 <= row
        assert 0 <= column
        assert row < self.height
        assert column < self.width
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

    def fill_borders(self):
        for i in range(self.width):
            self.set_element_at(0, i, GridObject.WALL)
            self.set_element_at(self.height - 1, i, GridObject.WALL)
        for i in range(self.height):
            self.set_element_at(i, 0, GridObject.WALL)
            self.set_element_at(i, self.width - 1, GridObject.WALL)


if __name__ == "__main__":
    a = Grid()
    a.fill_borders()
    a[(2, 2)] = GridObject.SNAKE_1

    b = Grid()
    b.deserialize(a.serialize())

    assert str(a) == str(b)
