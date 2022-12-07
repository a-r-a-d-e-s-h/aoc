#pt 1: 4:51
#pt 2: 6:15

def get_input():
    data = open("input.txt").read().split("\n\n")
    return data

def main():
    data = get_input()

    totals = []
    for chunk in data:
        totals.append(sum(map(int, chunk.splitlines())))
    print(max(totals))

    totals.sort(reverse=True)
    print(sum(totals[:3]))


if __name__ == "__main__":
    main()
