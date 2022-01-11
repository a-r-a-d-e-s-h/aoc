def part_1(instructions):
    pos = [0, 0]
    aim = 0

    for direction, dist in instructions:
        if direction == "forward":
            pos[0] += dist
        elif direction == "down":
            pos[1] += dist
        elif direction == "up":
            pos[1] -= dist
    
    print(pos[0] * pos[1])

def part_2(instructions):
    pos = [0, 0]
    aim = 0

    for direction, dist in instructions:
        if direction == "forward":
            pos[0] += dist
            pos[1] += aim*dist
        elif direction == "down":
            aim += dist
        elif direction == "up":
            aim -= dist
    
    print(pos[0] * pos[1])


if __name__ == "__main__":
    lines = open("input.txt").read().splitlines()
    instructions = [
        (direction, int(dist)) for direction, dist in map(str.split, lines)
    ]

    part_1(instructions)
    part_2(instructions)
