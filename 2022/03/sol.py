#!/usr/bin/env python3.10

# Forgot to start time until about 2 mins
# 8:16 + ~2 mins
# 14:18 + ~2 mins

def get_input():
    text = open("input.txt").read()
    text = text.rstrip("/n")
    lines = text.splitlines()
    return lines

def process_compartments(item):
    n = len(item)
    assert n%2 == 0
    size = n//2
    return (item[:size], item[size:])

def priority(x):
    if 'a' <= x <= 'z':
        return ord(x) - ord('a') + 1
    if 'A' <= x <= 'Z':
        return ord(x) - ord('A') + 27


def part_1(data):
    data = [process_compartments(item) for item in data]
    total = 0
    for item in data:
        c1, c2 = item
        intersection = set(c1).intersection(c2)
        assert len(intersection) == 1
        total += priority(intersection.pop())
    return total


def part_2(data):
    total = 0
    while data:
        r1, r2, r3 = data[:3]
        data = data[3:]
        total += priority(set(r1).intersection(r2, r3).pop())
    return total

def main():
    data = get_input()

    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
