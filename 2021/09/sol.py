def solutions(data):
    width = len(data[0])
    height = len(data)

    def nbours(x, y):
        x_min = max(x - 1, 0)
        x_max = min(x + 1, width - 1)
        y_min = max(y - 1, 0)
        y_max = min(y + 1, height - 1)
        for i in range(x_min, x_max + 1):
            if i != x:
                yield (i, y)

        for j in range(y_min, y_max + 1):
            if j != y:
                yield (x, j)

    total = 0

    minima = []

    for y in range(height):
        for x in range(width):
            val = data[y][x]
            for nx, ny in nbours(x, y):
                if data[ny][nx] <= val:
                    break
            else:
                total += val + 1
                minima.append((x, y))

    yield total

    def compute_basin(x, y):
        basin = [(x, y)]
        remaining = [(x, y)]

        while remaining:
            x0, y0 = remaining.pop()
            val = data[y0][x0]
            for nx, ny in nbours(x0, y0):
                if (nx, ny) in basin:
                    continue
                nval = data[ny][nx]
                if nval >= val and nval < 9:
                    remaining.append((nx, ny))
                    basin.append((nx, ny))
        return basin

    basin_sizes = []

    for x, y in minima:
        basin_sizes.append(len(compute_basin(x, y)))

    basin_sizes.sort(reverse=True)
    a, b, c = basin_sizes[:3]
    yield a*b*c


def main():
    data = open("input.txt").read().strip().splitlines()
    data = [list(map(int, line)) for line in data]
    
    for solution in solutions(data):
        print(solution)


if __name__ == "__main__":
    main()
