#!/usr/bin/env python3.10

#14:45
#19:52

import re

class Stack:
    def __init__(self, text_input):
        self.text_input = text_input
        self.parse_text()

    def parse_text(self):
        lines = self.text_input.splitlines()
        last_line = lines[-1]
        self.num_stacks = int(last_line.split()[-1])

        self.stacks = [list() for __ in range(self.num_stacks)]

        for line in lines[:-1]:
            stack = 0
            while line:
                if line[0] == '[':
                    term = line[1]
                    self.stacks[stack].insert(0, term)
                line = line[4:]
                stack += 1

    def parse_instruction(self, instruction):
        res = re.match("move (\d+) from (\d+) to (\d+)", instruction)
        return map(int, res.groups())

    def perform_instruction_9000(self, instruction):
        n, source, target = self.parse_instruction(instruction)

        for __ in range(n):
            self.move(source-1, target-1, 1)

    def perform_instruction_9001(self, instruction):
        n, source, target = self.parse_instruction(instruction)
        self.move(source-1, target-1, n)

    def move(self, source, target, n):
        to_move = self.stacks[source][-n:]
        self.stacks[source] = self.stacks[source][:-n]
        self.stacks[target].extend(to_move)


def get_data():
    data = open("input.txt").read().rstrip("\n")
    stack, moves = data.split("\n\n")

    return stack, moves.splitlines()


def main():
    stack_raw, moves = get_data()
    stack = Stack(stack_raw)
    for mov in moves:
        stack.perform_instruction_9000(mov)

    print(''.join(item[-1] for item in stack.stacks))

    stack = Stack(stack_raw)
    for mov in moves:
        stack.perform_instruction_9001(mov)

    print(''.join(item[-1] for item in stack.stacks))

if __name__ == "__main__":
    main()
