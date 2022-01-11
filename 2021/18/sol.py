from itertools import product


class Pair:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        self.val1.parent = self
        self.val2.parent = self
        self.parent = None

    def reduce(self):
        while 1:
            changes = False
            while self.explode():
                changes = True
            if self.split():
                changes = True

            if not changes:
                break

    def explode(self):

        # Find exploding pair
        def find_exploding(pair, depth=0):
            val1 = pair.val1
            if isinstance(val1, Pair):
                exploding = find_exploding(val1, depth+1)
                if exploding is not None:
                    return exploding

            val2 = pair.val2
            if isinstance(val2, Pair):
                exploding = find_exploding(val2, depth+1)
                if exploding is not None:
                    return exploding

            if isinstance(val1, Regular) and isinstance(val2, Regular):
                if depth >= 4:
                    return pair
                else:
                    return None
            return None

        to_explode = find_exploding(self)
        if to_explode is None:
            return None

        left = to_explode.find_left_regular()
        if left is not None:
            left.val += to_explode.val1.val
        
        right = to_explode.find_right_regular()
        if right is not None:
            right.val += to_explode.val2.val

        parent = to_explode.parent
        if parent is None:
            print(to_explode, self)
        if parent.val1 == to_explode:
            parent.val1 = Regular(0)
            parent.val1.parent = parent
        else:
            parent.val2 = Regular(0)
            parent.val2.parent = parent

        return to_explode

    def split(self):
        val1 = self.val1
        if isinstance(val1, Regular):
            if val1.val >= 10:
                self.val1 = Pair(
                    Regular(val1.val//2),
                    Regular(val1.val - val1.val//2)
                )
                self.val1.parent = self
                return self.val1
        else:
            splitted = val1.split()
            if splitted:
                return splitted

        val2 = self.val2
        if isinstance(val2, Regular):
            if val2.val >= 10:
                self.val2 = Pair(
                    Regular(val2.val//2),
                    Regular(val2.val - val2.val//2)
                )
                self.val2.parent = self
                return self.val2
        else:
            splitted = val2.split()
            if splitted:
                return splitted

        return None

    def magnitude(self):
        val1 = self.val1

        if isinstance(val1, Regular):
            v1_mag = val1.val
        else:
            v1_mag = val1.magnitude()

        val2 = self.val2
        if isinstance(val2, Regular):
            v2_mag = val2.val
        else:
            v2_mag = val2.magnitude()
        return 3*v1_mag + 2*v2_mag


    def find_left_regular(self):
        if not self.parent:
            return None
        parent = self.parent
        if parent.val2 == self:
            if isinstance(parent.val1, Regular):
                return parent.val1
            else:
                return parent.val1.last_regular_value()
        else: # parent.val1 == self
            return parent.find_left_regular()

    def find_right_regular(self):
        if not self.parent:
            return None
        parent = self.parent
        if parent.val1 == self:
            if isinstance(parent.val2, Regular):
                return parent.val2
            else:
                return parent.val2.first_regular_value()
        else:   # parent.val2 == self
            return parent.find_right_regular()

    def last_regular_value(self):
        val2 = self.val2
        if isinstance(val2, Regular):
            return val2
        else:
            return val2.last_regular_value()

    def first_regular_value(self):
        val1 = self.val1
        if isinstance(val1, Regular):
            return val1
        else:
            return val1.first_regular_value()

    def __str__(self):
        return "[" + str(self.val1) + "," + str(self.val2) + "]"



class Regular:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class Parser:
    def __init__(self, source):
        self.source = source
        self.pos = 0


    def get_number(self):
        matches = []
        while self.source[self.pos] in "0123456789":
            matches.append(self.source[self.pos])
            self.pos += 1

        if matches:
            return int("".join(matches))
        else:
            return None


    def parse_pair_or_val(self):
        matching_digits = []

        regular_digit = self.get_number()

        if regular_digit is not None:
            return Regular(regular_digit)

        if self.source[self.pos] != "[":
            raise RuntimeError("Expected [ at position {}".format(self.pos))
        self.pos += 1
        val1  = self.parse_pair_or_val()
        if self.source[self.pos] != ",":
            raise RuntimeError("Expected , at position {}".format(self.pos))
        self.pos += 1
        val2 = self.parse_pair_or_val()
        if self.source[self.pos] != "]":
            raise RuntimeError("Expected ]")
        self.pos += 1

        pair = Pair(val1, val2)
        val1.parent = pair
        val2.parent = pair
        return pair


def part_1(lines):
    # 93:37
    total = Parser(lines[0]).parse_pair_or_val()
    for line in lines[1:]:
        total = Pair(total, Parser(line).parse_pair_or_val())
        total.reduce()

    return total.magnitude()

def part_2(lines):
    # 103:23
    largest_mag = 0
    line_nums = range(len(lines))
    for x, y in product(line_nums, repeat=2):
        if x == y:
            continue
        x = lines[x]
        y = lines[y]

        x = Parser(x).parse_pair_or_val()
        y = Parser(y).parse_pair_or_val()
        pair = Pair(x, y)
        pair.reduce()
        mag = pair.magnitude()
        largest_mag = max(largest_mag, mag)
    return largest_mag


def main():
    data = open("input.txt").read().strip().splitlines()
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
