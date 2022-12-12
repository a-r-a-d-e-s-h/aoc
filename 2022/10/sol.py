#!/usr/bin/env python3.10

# 18:16
# 30:50

def get_input():
    text = open("input.txt").read().rstrip("\n")
    return text


class CPU:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 1
        self.cycle = 1

    def execute(self, line):
        if line == "noop":
            self.tick()
        elif line.startswith("addx "):
            self.tick(2)
            val = int(line[len("addx "):])
            self.x += val

    def tick(self, n=1):
        for i in range(n):
            self.tick_once()

    def tick_once(self):
        self.during_tick()
        self.cycle += 1
        self.after_tick()

    def during_tick(self):
        pass

    def after_tick(self):
        pass


class Part1(CPU):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sol = 0

    def during_tick(self):
        if self.cycle in [20, 60, 100, 140, 180, 220]:

            strength = self.cycle * self.x
            self.sol += strength


class Part2(CPU):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = [[0]*40 for __ in range(6)]

    def display_as_text(self):
        lines = []
        for row in self.display:
            chars = ["|"] + ["#" if val else " " for val in row] + ["|"]
            lines.append(" ".join(chars))
        border = "+" + "-"*81 + "+"
        lines = [border] + lines + [border]
        return "\n".join(lines)

    def during_tick(self):
        cycles = self.cycle - 1
        col = cycles % 40
        row = (cycles // 40) % 6

        if self.x - 1 <= col <= self.x + 1:
            self.display[row][col] = 1


def main():
    text = get_input()

    lines = text.splitlines()
    cpu = Part1()
    for line in lines:
        cpu.execute(line)

    print(cpu.sol)

    cpu = Part2()
    for line in lines:
        cpu.execute(line)

    print(cpu.display_as_text())


if __name__ == "__main__":
    main()
