#!/usr/bin/env python3.10

# 33:32
# 38:31

def get_input():
    text = open("input.txt").read().rstrip()
    return text

class Layout:
    def __init__(self, text):
        self.start = None
        self.end = None
        self.grid = None
        self.parse_text(text)

    def parse_text(self, text):
        lines = text.splitlines()
        grid = []
        self.grid = grid

        for row_num, line in enumerate(lines):
            row = []
            grid.append(row)
            for col, char in enumerate(line):
                if char == 'S':
                    self.start = (row_num, col)
                    char = 'a'
                elif char == 'E':
                    self.end = (row_num, col)
                    char = 'z'
                row.append(ord(char) - ord('a'))

        self.height = len(grid)
        self.width = len(grid[0])

    def valid_targets_from(self, row, col):
        current_val = self.grid[row][col]

        for r0, c0 in self.all_nbours(row, col):
            if self.grid[r0][c0] - current_val >= -1:
                yield (r0, c0)

    def all_nbours(self, row, col):
        for r0 in range(max(0, row - 1), min(self.height, row + 2)):
            for c0 in range(max(0, col - 1), min(self.width, col + 2)):
                if (r0 == row) != (c0 == col):
                    yield (r0, c0)

    def calculate_all_paths(self):
        shortest_paths = {self.end: 0}
        to_do = [self.end]

        while to_do:
            source = to_do.pop(0)
            for target in self.valid_targets_from(*source):
                if target not in shortest_paths:
                    shortest_paths[target] = shortest_paths[source] + 1
                    to_do.append(target)
        return shortest_paths


def main():
    text = get_input()
    layout = Layout(text)

    distances = layout.calculate_all_paths()
    print(distances[layout.start])

    shortest = float('inf')
    for row in range(layout.height):
        for col in range(layout.width):
            if layout.grid[row][col] == 0:
                shortest = min(
                    shortest, distances.get((row, col), float('inf'))
                )

    print(shortest)


if __name__ == "__main__":
    main()
