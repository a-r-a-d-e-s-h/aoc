from collections import Counter
import re

def display_image(image):
    keys = list(image.keys())
    min_row = min(key[0] for key in keys)
    max_row = max(key[0] for key in keys)
    min_col = min(key[1] for key in keys)
    max_col = max(key[1] for key in keys)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if image[row, col]:
                print("#", end='')
            else:
                print(".", end='')
        print()


def compute(alg, data, iters):
    image = Counter()
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col]:
                image[row, col] = 1

    # Anything that diagonally touches a light pixel must be included in the
    # image for executing the algorithm.

    def nbours(row, col):
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                yield (r, c)

    def bleed(image):
        copy = image.copy()
        for row, col in image:
            if not image[row, col]:
                # Only need to bleed for light pixels
                continue

            for nbour in nbours(row, col):
                if nbour not in copy:
                    copy[nbour] = 0
                    assert nbour in copy
        return copy

    # What do 000000000 and 111111111 map to?
    if alg[0] == 0:
        do_swap = False
    else:
        assert alg[2**9 - 1] == 0
        do_swap = True


    for index in range(iters):
        image = bleed(image)
        new_image = Counter()
        for row, col in image:
            region = []
            for i, j in nbours(row, col):
                region.append(image[i, j])
            key = ''.join(map(str, region))
            key = int(key, 2)
            if do_swap and index%2 == 1:
                # If index is odd, and do_swap is true, then we're in reflected
                # mode.
                key ^= (2**9 - 1)
            if do_swap and index%2 == 0:
                # We have to reflect
                if alg[key] == 0:
                    new_image[row, col] = 1
            else:
                if alg[key]:
                    new_image[row, col] = 1
        image = new_image

    return sum(image.values())


def part_1(alg, data):
    # 64:50
    return compute(alg, data, 2)


def part_2(alg, data):
    # 66:27
    return compute(alg, data, 50)


def main():
    data = open("input.txt").read().strip()
    alg, data = data.split('\n\n')
    alg = re.sub("\n", '', alg)
    data = data.splitlines()

    alg = [0 if char == '.' else 1 for char in alg]
    data = [[0 if char == '.' else 1 for char in line] for line in data]

    print(part_1(alg, data))
    print(part_2(alg, data))


if __name__ == "__main__":
    main()
