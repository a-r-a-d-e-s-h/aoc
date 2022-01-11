from collections import Counter


def main():
    lines = open("input.txt").read().splitlines()
    
    len_row = len(lines[0])

    bits_most_common = ""
    bits_least_common = ""

    for i in range(len_row):
        c = Counter(l[i] for l in lines)
        if c["0"] > c["1"]:
            bits_most_common += "0"
            bits_least_common += "1"
        else:
            bits_most_common += "1"
            bits_least_common += "0"

    print(int(bits_most_common, 2) * int(bits_least_common, 2))

    # 4:13

    oxygen_genorator_rating = None
    co2_scrubbing_rating = None

    bit_position = 0

    remaining_lines = lines.copy()

    for i in range(len_row):
        bits_in_position = [l[i] for l in remaining_lines]
        c = Counter(bits_in_position)
        if c["0"] > c["1"]:
            most_common = "0"
        else:
            # If equal, we go with 1
            most_common = "1"

        remaining_lines = [
            l for l in remaining_lines if l[i] == most_common
        ]
        if len(remaining_lines) == 1:
            break

    oxygen_generator_rating = int(remaining_lines[0], 2)

    remaining_lines = lines.copy()

    for i in range(len_row):
        bits_in_position = [l[i] for l in remaining_lines]
        c = Counter(bits_in_position)
        if c["0"] > c["1"]:
            least_common = "1"
        else:
            # If equal, we go with 0
            least_common = "0"

        remaining_lines = [
            l for l in remaining_lines if l[i] == least_common
        ]
        if len(remaining_lines) == 1:
            break

    co2_scrubber_rating = int(remaining_lines[0], 2)

    print(oxygen_generator_rating * co2_scrubber_rating)

    # 14:22


if __name__ == "__main__":
    main()
