from collections import Counter
from itertools import permutations


digit_map = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def part_1(data):
    # 12:03
    total = 0
    all_lengths = []
    length_counts = Counter()
    for digits, output in data:
        length_counts.update(map(len, output))

    return sum(length_counts[i] for i in [2, 4, 3, 7])


def deduce_digit_map(digits):
    all_chars = "abcdefg"

    real_digits = [set(dig) for dig in digit_map.values()]

    def map_perm(digit, perm):
        res = []
        for char in digit:
            index = all_chars.index(char)
            res.append(perm[index])
        return ''.join(res)

    for perm in permutations(all_chars):
        if all(set(map_perm(digit, perm)) in real_digits for digit in digits):
            break

    new_map = {}
    for i in range(10):
        real_digit = digit_map[i]
        for digit in digits:
            if set(map_perm(digit, perm)) == set(real_digit):
                new_map[i] = digit
    return new_map


def compute_output_vals(digits, output):
    digit_map = deduce_digit_map(digits)
    val = 0
    for digit in output:
        val *= 10
        val += sum(i for i in digit_map if set(digit_map[i]) == set(digit))
    return val


def part_2(data):
    # 47:16
    return sum(compute_output_vals(*entry) for entry in data)


def main():
    data = open("input.txt").read().strip().splitlines()
    data = [line.split("|") for line in data]
    data = [[part.split() for part in entry] for entry in data]
    print(part_1(data))
    print(part_2(data))

if __name__ == "__main__":
    main()
