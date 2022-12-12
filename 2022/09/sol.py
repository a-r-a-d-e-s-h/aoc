#!/usr/bin/env python3.10

# 13:03
# 34:19

def get_input():
    text = open("input.txt").read().rstrip()
    return text


class Grid:
    def __init__(self, knots=1):
        self.head = (0, 0)
        self.tails = [(0, 0)]*knots
        self.knots = knots

    def reset(self):
        self.head = (0, 0)
        self.tails = [(0, 0)]*knots

    def move_head(self, direction):
        if direction == 'R':
            self.head = (self.head[0] + 1, self.head[1])
        if direction == 'L':
            self.head = (self.head[0] - 1, self.head[1])
        if direction == 'U':
            self.head = (self.head[0], self.head[1] - 1)
        if direction == 'D':
            self.head = (self.head[0], self.head[1] + 1)

        self.adjust_tails()
    
    def adjust_tails(self):
        for i, tail in enumerate(self.tails):
            if i == 0:
                head = self.head
            else:
                head = self.tails[i-1]

            while 1:
                dist_x = abs(tail[0] - head[0])
                dist_y = abs(tail[1] - head[1])

                if dist_x <= 1 and dist_y <= 1:
                    self.tails[i] = tail
                    break

                dx = head[0] - tail[0]
                dy = head[1] - tail[1]

                if dx:
                    new_tail_x = tail[0] + dx//abs(dx)
                else:
                    new_tail_x = tail[0]

                if dy:
                    new_tail_y = tail[1] + dy//abs(dy)
                else:
                    new_tail_y = tail[1]
                tail = (new_tail_x, new_tail_y)

def main():
    text = get_input()

    # Part 1
    grid = Grid()
    visited = set([grid.tails[0]])

    moves = text.splitlines()
    moves = [item.split() for item in moves]
    moves = [(direction, int(dist)) for direction, dist in moves]

    for direction, dist in moves:
        for i in range(dist):
            grid.move_head(direction)
            visited.add(grid.tails[0])
    print(len(visited))

    # Part 2
    grid = Grid(knots=9)
    visited = set([grid.tails[8]])
    for direction, dist in moves:
        for i in range(dist):
            grid.move_head(direction)
            visited.add(grid.tails[8])
    print(len(visited))



if __name__ == "__main__":
    main()
