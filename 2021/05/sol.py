from collections import Counter, defaultdict
import operator


class Vector(tuple):
    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __add__(self, rhs):
        return type(self)(*map(operator.__add__, self, rhs))

    def __neg__(self):
        return type(self)(*map(operator.__neg__, self))

    def __sub__(self, rhs):
        return self + -rhs


def part_1(data):
    # 9:16
    grid = defaultdict(int)
    for start, end in data:
        if start[0] == end[0]:
            x = start[0]
            y0 = min(start[1], end[1])
            y1 = max(start[1], end[1])
            for y in range(y0, y1+1):
                grid[(x, y)] += 1
        elif start[1] == end[1]:
            y = start[1]
            x0 = min(start[0], end[0])
            x1 = max(start[0], end[0])
            for x in range(x0, x1+1):
                grid[(x, y)] += 1

    counts = Counter(grid)
    return sum(counts[x] > 1 for x in counts)


def part_2(data):
    # 14:35
    grid = defaultdict(int)
    for start, end in data:
        if start[0] == end[0]:
            x = start[0]
            y0 = min(start[1], end[1])
            y1 = max(start[1], end[1])
            for y in range(y0, y1+1):
                grid[(x, y)] += 1
        elif start[1] == end[1]:
            y = start[1]
            x0 = min(start[0], end[0])
            x1 = max(start[0], end[0])
            for x in range(x0, x1+1):
                grid[(x, y)] += 1
        elif (
            start[0] - end[0] == start[1] - end[1]
            or
            start[0] - end[0] == end[1] - start[1]
        ):
            diff_x = end[0] - start[0]
            diff_y = end[1] - start[1]
            if diff_x > 0:
                dx = 1
            else:
                dx = -1

            if diff_y > 0:
                dy = 1
            else:
                dy = -1

            current_pos = start
            while current_pos != end:
                grid[tuple(current_pos)] += 1
                current_pos += (dx, dy)
            grid[tuple(current_pos)] += 1
    counts = Counter(grid)
    return sum(counts[x] > 1 for x in counts)



def main():
    data = open("input.txt").read().splitlines()
    data = [line.split("->") for line in data if line]
    data = [[Vector(*map(int, x.split(','))) for x in entry] for entry in data]

    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
