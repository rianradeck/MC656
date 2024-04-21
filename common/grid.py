import enum


class GridObject(enum.Enum):
    EMPTY = 0
    WALL = 1
    SNAKE_1 = 2
    SNAKE_2 = 3
    APPLE = 4


class Grid:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.data = [0] * (self.width * self.height)

    def serialize(self):
        assert 0 < self.width
        assert 0 < self.height
        assert self.width < 256
        assert self.height < 256
        return bytes(self.data)

    def deserialize(self, byte_str):
        self.data = list(map(int, byte_str))

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
                ret += str(self.element_at(i, j))
            ret += "\n"
        return ret
