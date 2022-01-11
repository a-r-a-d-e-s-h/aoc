from itertools import count


def iterate_octopuses(octopuses):
    # Increase all by 1

    width = len(octopuses[0])
    height = len(octopuses)

    def nbours(x, y):
        x_min = max(0, x-1)
        x_max = min(width-1, x + 1)
        y_min = max(0, y-1)
        y_max = min(height-1, y + 1)

        for x0 in range(x_min, x_max + 1):
            for y0 in range(y_min, y_max + 1):
                if x0 != x or y0 != y:
                    yield x0, y0

    for row in range(height):
        for col in range(width):
            octopuses[row][col] += 1

    flashed = []
    while 1:
        to_flash = []
        for row in range(height):
            for col in range(width):
                if octopuses[row][col] > 9:
                    if (row, col) not in flashed:
                        to_flash.append((row, col))
        for row, col in to_flash:
            if (row, col) in flashed:
                continue
            flashed.append((row, col))
            for r0, c0 in nbours(row, col):
                octopuses[r0][c0] += 1

        if not to_flash:
            break

    for row, col in flashed:
        octopuses[row][col] = 0

    return len(flashed)


def part_1(octopuses):
    # 13:39
    # Copy it:
    octopuses = [row.copy() for row in octopuses]
    total = 0
    for __ in range(100):
        total += iterate_octopuses(octopuses)
    return total


def part_2(octopuses):
    # 18:28
    octopuses = [row.copy() for row in octopuses]
    total = len(octopuses) * len(octopuses[0])

    for step in count(start=1):
        flashed = iterate_octopuses(octopuses)
        if flashed == total:
            return step


def main():
    data = open("input.txt").read().strip().splitlines()
    octopuses = [list(map(int, line)) for line in data]

    print(part_1(octopuses))
    print(part_2(octopuses))


if __name__ == "__main__":
    main()
