def part_1(points, folds):
    # 17:53
    all_points = set(points)

    axis, val = folds[0]
    new_points = set()
    if axis == "x":
        for point in all_points:
            if point[0] <= val:
                new_points.add(point)
            else:
                new_points.add((2*val - point[0], point[1]))
    elif axis == "y":
        for point in all_points:
            if point[1] <= val:
                new_points.add(point)
            else:
                new_points.add((point[0], 2*val - point[1]))
    return len(new_points)


def part_2(points, folds):
    # 22:05
    for axis, val in folds:
        points = set(points)
        new_points = set()
        if axis == "x":
            for point in points:
                if point[0] <= val:
                    new_points.add(point)
                else:
                    new_points.add((2*val - point[0], point[1]))
        elif axis == "y":
            for point in points:
                if point[1] <= val:
                    new_points.add(point)
                else:
                    new_points.add((point[0], 2*val - point[1]))
        points = new_points

    min_x = min(pt[0] for pt in points)
    max_x = max(pt[0] for pt in points)
    min_y = min(pt[1] for pt in points)
    max_y = max(pt[1] for pt in points)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()

def main():
    data = open("input.txt").read().strip()
    pairs, folds = data.split("\n\n")
    pairs = pairs.splitlines()
    folds = folds.splitlines()

    pairs = [tuple(map(int, line.split(","))) for line in pairs]
    folds = [fold.split(" ")[-1] for fold in folds]
    folds = [fold.split("=") for fold in folds]
    folds = [(axis, int(val)) for axis, val in folds]
    print(part_1(pairs, folds))
    part_2(pairs, folds)


if __name__ == "__main__":
    main()
