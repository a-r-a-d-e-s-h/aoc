def main():
    data = open("input.txt").read().strip()
    vals = list(map(int, data.split(',')))

    min_val = min(vals)
    max_val = max(vals)

    test_range = range(min_val, max_val + 1)

    def required_fuel_pt1(vals, pos):
        return sum(abs(val - pos) for val in vals)

    print(min(required_fuel_pt1(vals, pos) for pos in test_range))

    def consec_sum(n):
        return n*(n + 1)//2

    def required_fuel_pt2(vals, pos):
        return sum(consec_sum(abs(val - pos)) for val in vals)

    print(min(required_fuel_pt2(vals, pos) for pos in test_range))


if __name__ == "__main__":
    main()
