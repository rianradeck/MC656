import enum


@enum.unique
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

    def __getitem__(self, key):
        return self.element_at(*key)

    def __setitem__(self, key, value):
        self.set_element_at(*key, value)

    def fill_borders(self):
        for i in range(self.width):
            self.set_element_at(0, i, GridObject.WALL.value)
            self.set_element_at(self.height - 1, i, GridObject.WALL.value)
        for i in range(self.height):
            self.set_element_at(i, 0, GridObject.WALL.value)
            self.set_element_at(i, self.width - 1, GridObject.WALL.value)


if __name__ == "__main__":
    a = Grid()
    a.fill_borders()
    a[(2, 2)] = GridObject.SNAKE_1.value

    print(a)
