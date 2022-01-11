from itertools import count


class Layout:
    east_symb = ">"
    south_symb = "v"
    empty_symb = '.'

    def __init__(self, grid):
        self.grid = list(list(line) for line in grid)
        self.height = len(grid)
        self.width = len(grid[0])

    def do_move(self):
        self.move_east()
        self.move_south()

    def move_east(self):
        grid = self.grid
        moves = []
        for pos in self.all_squares():
            if self.get_pos(pos) == self.east_symb:
                east_of = self.east_of(pos)
                if self.get_pos(east_of) == self.empty_symb:
                    moves.append((pos, east_of))
        for source, target in moves:
            self.set_pos(source, self.empty_symb)
            self.set_pos(target, self.east_symb)

    def move_south(self):
        grid = self.grid
        moves = []
        for pos in self.all_squares():
            if self.get_pos(pos) == self.south_symb:
                south_of = self.south_of(pos)
                if self.get_pos(south_of) == self.empty_symb:
                    moves.append((pos, south_of))
        for source, target in moves:
            self.set_pos(source, self.empty_symb)
            self.set_pos(target, self.south_symb)

    def get_pos(self, coord):
        return self.grid[coord[0]][coord[1]]

    def set_pos(self, coord, val):
        self.grid[coord[0]][coord[1]] = val

    def all_squares(self):
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col)

    def east_of(self, pos):
        row, col = pos
        col = (col + 1) % self.width
        return row, col

    def south_of(self, pos):
        row, col = pos
        row = (row + 1) % self.height
        return row, col

    def display(self):
        lines = []
        for row in self.grid:
            lines.append("".join(row))
        return "\n".join(lines)


def part_1(data):
    # 14:26
    layout = Layout(data)
    last_pos = layout.display()
    for step in count(start=1):
        layout.do_move()
        pos = layout.display()
        if pos == last_pos:
            return step
        else:
            last_pos = pos


def main():
    data = open("input.txt").read().strip()
    lines = data.splitlines()
    print(part_1(lines))


if __name__ == "__main__":
    main()
