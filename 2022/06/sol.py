#!/usr/bin/env python3.10

# 2:26
# 3:11

def get_input():
    text = open("input.txt").read().rstrip("\n")
    return text


def main():
    text = get_input()

    for i in range(len(text)):
        if len(set(text[i:i+4])) == 4:
            print(i+4)
            break

    for i in range(len(text)):
        if len(set(text[i:i+14])) == 14:
            print(i+14)
            break


if __name__ == "__main__":
    main()
