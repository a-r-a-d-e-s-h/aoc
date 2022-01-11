from collections import defaultdict


def part_1(data):
    # 10:40
    def paths_a_to_b(a, b, exclude=set()):
        """Compute how many paths from a to b which avoid exclude"""
        if a == b:
            return 1
        exclude = exclude.copy()
        if a.islower():
            exclude.add(a)
        total = 0
        for destination in data[a]:
            if destination not in exclude:
                total += paths_a_to_b(destination, b, exclude=exclude)
        return total

    return paths_a_to_b("start", "end")


def part_2(data):
    # 16:35
    def paths_a_to_b(a, b, exclude=set(), allow_repeat=True):
        """Compute how many paths from a to b which avoid exclude"""
        if a == b:
            return 1
        exclude = exclude.copy()
        if a.islower():
            exclude.add(a)
        total = 0
        for destination in data[a]:
            if destination not in exclude:
                total += paths_a_to_b(destination, b, exclude, allow_repeat)
            else:
                if allow_repeat:
                    if destination not in ("start", "end"):
                        total += paths_a_to_b(destination, b, exclude, False)
        return total

    return paths_a_to_b("start", "end")


def main():
    data = open("input.txt").read().strip().splitlines()

    paths = defaultdict(list)

    for item in data:
        x, y = item.split("-")
        paths[x].append(y)
        paths[y].append(x)

    print(part_1(paths))
    print(part_2(paths))


if __name__ == "__main__":
    main()
