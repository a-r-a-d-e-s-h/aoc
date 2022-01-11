from itertools import chain
import re


def lmap(*args):
    return list(map(*args))


class BingoBoard:
    def __init__(self, data):
        self.rows = [
            lmap(int, re.findall("\d+", line)) for line in data.splitlines()
        ]
        self.cols = list(zip(*self.rows))
        self.all_numbers = list(chain.from_iterable(self.rows))

    def is_winning(self, called_numbers):
        # Check rows
        for array in [self.rows, self.cols]:
            for row in array:
                if set(row).issubset(called_numbers):
                    return True
        return False

    def compute_score(self, called_numbers):
        num = called_numbers[-1]
        return sum(set(self.all_numbers).difference(called_numbers))*num


def part_1(boards, called_numbers):
    for i in range(len(called_numbers)):
        for board in boards:
            if board.is_winning(called_numbers[:i+1]):
                return board.compute_score(called_numbers[:i+1])


def part_2(boards, called_numbers):
    for i in range(len(called_numbers)):
        winning_boards = []
        for board in boards:
            if board.is_winning(called_numbers[:i+1]):
                boards.remove(board)
                winning_boards.append(board)
        if not boards:
            return winning_boards[0].compute_score(called_numbers[:i+1])


def main():
    data = open("input.txt").read()

    data = data.split("\n\n")
    called_numbers = lmap(int, data[0].split(','))
    boards = [BingoBoard(block) for block in data[1:]]

    print(part_1(boards, called_numbers))
    print(part_2(boards, called_numbers))


if __name__ == "__main__":
    main()
