import math


class Parser:
    class OPERATOR:
        SUM = 0
        PRODUCT = 1
        MINIMUM = 2
        MAXIMUM = 3
        GREATER_THAN = 5
        LESS_THAN = 6
        EQUAL_TO = 7

    def __init__(self, data_string=None, bits=None):
        if data_string:
            self.stream = self.to_bits(data_string)
        else:
            self.stream = iter(bits)
        self.version_sum = 0

    def to_bits(self, data):
        for char in data:
            val = int(char, 16)
            bit_string = "{:04b}".format(val)
            bits = map(int, bit_string)
            yield from bits

    def get_n_bits(self, n):
        ret = []
        for __ in range(n):
            ret.append(next(self.stream))
        return ret

    def n_bits_to_int(self, n, stream=None):
        if stream is None:
            stream = self.stream
        ret = 0
        for __ in range(n):
            ret *= 2
            ret += next(stream)
        return ret

    def bits_to_int(self, stream):
        val = 0
        for bit in stream:
            val *= 2
            val += bit
        return val

    def get_literal_value(self):
        bits_for_val = []
        while 1:
            chunk = self.get_n_bits(5)
            bits_for_val.extend(chunk[1:])
            if chunk[0] == 0:
                break
        return self.bits_to_int(bits_for_val)

    def parse_packet(self):
        ver = self.n_bits_to_int(3)
        self.version_sum += ver
        type_id = self.n_bits_to_int(3)
        if type_id == 4:
            return self.get_literal_value()
        else:
            sub_vals = []
            length_type_id = self.n_bits_to_int(1)
            if length_type_id == 0:
                length = self.n_bits_to_int(15)
                new_parser = Parser(bits=self.get_n_bits(length))
                while 1:
                    try:
                        val = new_parser.parse_packet()
                    except StopIteration:
                        break
                    else:
                        sub_vals.append(val)
                self.version_sum += new_parser.version_sum
            else:
                length = self.n_bits_to_int(11)
                for __ in range(length):
                    sub_vals.append(self.parse_packet())

            if type_id == self.OPERATOR.SUM:
                return sum(sub_vals)
            elif type_id == self.OPERATOR.PRODUCT:
                return math.prod(sub_vals)
            elif type_id == self.OPERATOR.MINIMUM:
                return min(sub_vals)
            elif type_id == self.OPERATOR.MAXIMUM:
                return max(sub_vals)
            elif type_id == self.OPERATOR.GREATER_THAN:
                return sub_vals[0] > sub_vals[1]
            elif type_id == self.OPERATOR.LESS_THAN:
                return sub_vals[0] < sub_vals[1]
            elif type_id == self.OPERATOR.EQUAL_TO:
                return sub_vals[0] == sub_vals[1]


def part_1(data):
    # 42:04
    parser = Parser(data)
    parser.parse_packet()
    return parser.version_sum


def part_2(data):
    # 49:24
    parser = Parser(data)
    return parser.parse_packet()

def main():
    data = open("input.txt").read().strip()
    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
