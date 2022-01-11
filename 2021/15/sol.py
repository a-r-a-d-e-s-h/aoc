from collections import defaultdict


def compute_path(data, start, end):
    height = data['height']
    width = data['width']
    def nbours(x, y):
        min_x = max(0, x-1)
        max_x = min(width-1, x+1)
        min_y = max(0, y-1)
        max_y = min(height-1, y+1)
        for x0 in range(min_x, max_x + 1):
            if x0 != x:
                yield x0, y
        for y0 in range(min_y, max_y + 1):
            if y0 != y:
                yield x, y0

    min_paths = defaultdict(lambda: float("inf"))

    min_paths[start] = 0
    done = defaultdict(int)

    done_nbours = {start}

    while not done[end]:
        best_dist = float('inf')
        best_nbour = None
        for nbour in done_nbours:
            if min_paths[nbour] < best_dist:
                best_dist = min_paths[nbour]
                best_nbour = nbour
        done[best_nbour] = 1
        done_nbours.remove(best_nbour)
        for nbour in nbours(*best_nbour):
            if not done[nbour]:
                done_nbours.add(nbour)
                min_paths[nbour] = min(
                    min_paths[nbour], min_paths[best_nbour] + data[nbour]
                )

    return min_paths[end]


def part_1(data):
    # 56:17
    # pt 2: 69:43
    height = data['height']
    width = data['width']
    return compute_path(data, (0, 0), (width-1, height-1))


def main():
    data = open("input.txt").read().strip().splitlines()
    array = {}
    for col, line in enumerate(data):
        for row, val in enumerate(line):
            array[row, col] = int(val)
    array['width'] = len(data[0])
    array['height'] = len(data)
    print(part_1(array))

    pt2_array = {}
    for x in range(5):
        for y in range(5):
            for col, line in enumerate(data):
                for row, val in enumerate(line):
                    pt2_array[
                        col + x*array['width'], row + y*array['height']
                    ] = (int(val) + x + y - 1)%9 + 1
    pt2_array['width'] = 5*array['width']
    pt2_array['height'] = 5*array['height']
    print(part_1(pt2_array))


if __name__ == "__main__":
    main()
