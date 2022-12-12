#!/usr/bin/env python3.10

# 7:01
# 12:49

def get_input():
    text = open("input.txt").read().rstrip()
    return text


def main():
    text = get_input()

    # Part 1
    grid = text.splitlines()
    width = len(grid[0])
    height = len(grid)

    visible = 0
    for row in range(height):
        for col in range(width):
            # Is the tree at grid[row][col] visible?
            # Check all four directions:
            tree = grid[row][col]
            for c0 in range(0, col):
                if grid[row][c0] >= tree:
                    break
            else:
                visible += 1
                continue

            for c0 in range(col + 1, width):
                if grid[row][c0] >= tree:
                    break
            else:
                visible += 1
                continue

            for r0 in range(0, row):
                if grid[r0][col] >= tree:
                    break
            else:
                visible += 1
                continue

            for r0 in range(row + 1, height):
                if grid[r0][col] >= tree:
                    break
            else:
                visible += 1
                continue
    print(visible)

    # part 2
    scenic_score = 0
    for row in range(height):
        for col in range(width):
            score = 1
            tree = grid[row][col]

            # For each direction, count how many we can see:
            factor = 0
            for c0 in range(col-1, -1, -1):
                factor += 1
                if grid[row][c0] >= tree:
                    break
            score *= factor

            factor = 0
            for c0 in range(col+1, width):
                factor += 1
                if grid[row][c0] >= tree:
                    break
            score *= factor

            factor = 0
            for r0 in range(row-1, -1, -1):
                factor += 1
                if grid[r0][col] >= tree:
                    break
            score *= factor

            factor = 0
            for r0 in range(row + 1, height):
                factor += 1
                if grid[r0][col] >= tree:
                    break
            score *= factor

            scenic_score = max(scenic_score, score)
    print(scenic_score)

if __name__ == "__main__":
    main()
