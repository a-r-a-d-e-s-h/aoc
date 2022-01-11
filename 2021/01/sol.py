def main():
    vals = list(map(int, open("input.txt")))
    print(sum(a < b for a, b in zip(vals, vals[1:])))
    summed_vals = list(map(sum, zip(vals, vals[1:], vals[2:])))
    print(sum(a < b for a, b in zip(summed_vals, summed_vals[1:])))


if __name__ == "__main__":
    main()
