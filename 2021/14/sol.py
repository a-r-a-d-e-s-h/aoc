from collections import Counter


def compute_diff(template, rules, n):
    pair_counts = Counter()
    pair_counts.update("".join(pair) for pair in zip(template, template[1:]))
    for __ in range(n):
        new_counts = Counter()
        for pair in pair_counts:
            if pair in rules:
                new_pair = pair[0] + rules[pair] + pair[1]
                new_counts[new_pair[:2]] += pair_counts[pair]
                new_counts[new_pair[1:]] += pair_counts[pair]
            else:
                new_counts[pair] += pair_counts[pair]
        pair_counts = new_counts

    counter = Counter()
    for pair in pair_counts:
        for char in pair:
            counter[char] += pair_counts[pair]

    # Each char is counted twice, except for the first and last ones of the
    # string, but after dividing by 2 that discrepency is lost.

    for char in counter:
        counter[char] //= 2

    return max(counter.values()) - min(counter.values())


def main():
    data = open("input.txt").read().strip()

    template, rules = data.split("\n\n")
    rules = rules.splitlines()
    rules = [rule.split("->") for rule in rules]
    rules = [[x.strip() for x in rule] for rule in rules]
    rules = {a: b for a, b in rules}

    print(compute_diff(template, rules, 10))
    print(compute_diff(template, rules, 40))

if __name__ == "__main__":
    main()
