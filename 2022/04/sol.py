#!/usr/bin/env python3.10

# 3:48
# 7:32

def get_input():
    text = open("input.txt").read().rstrip("\n")
    data = text.splitlines()
    return data

def main():
    lines = get_input()
    total = 0

    data = [
        [tuple(map(int, item.split('-'))) for item in line.split(',')]
        for line in lines
    ]
    for r1, r2 in data:
        if r1[0] <= r2[0] <= r2[1] <= r1[1]:
            total += 1
        elif r2[0] <= r1[0] <= r1[1] <= r2[1]:
            total += 1
    print(total)

    total = 0
    for r1, r2 in data:
        if set(range(r1[0], r1[1]+1)).intersection(range(r2[0], r2[1] + 1)):
            total += 1
    print(total)

if __name__ == "__main__":
    main()
