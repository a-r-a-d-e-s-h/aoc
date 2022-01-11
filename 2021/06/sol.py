from collections import Counter

def solve(vals):
    # 9:43
    fish_times = Counter(vals)
    def iterate_fish(times):
        results = Counter()
        for i in range(1, 9):
            results[i-1] = times[i]
        results[8] += times[0]
        results[6] += times[0]
        return results

    for i in range(80):
        fish_times = iterate_fish(fish_times)

    print(sum(fish_times.values()))

    for i in range(256 - 80):
        fish_times = iterate_fish(fish_times)

    print(sum(fish_times.values()))


def main():
    data = open("input.txt").read().strip().split(',')
    vals = list(map(int, data))
    solve(vals)



if __name__ == "__main__":
    main()
