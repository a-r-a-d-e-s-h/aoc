from itertools import product
import operator


class Parser:
    def __init__(self, lines):
        self.instructions = [self.parse_instruction(line) for line in lines]

    def parse_instruction(self, line):
        parts = line.split()
        name = parts[0]
        params = parts[1:]
        for i, val in enumerate(params):
            if not val in 'wxyz':
                params[i] = int(val)

        return (parts[0], params)

    def count_inputs(self):
        inputs = 0
        for inst in self.instructions:
            if inst[0] == 'inp':
                inputs += 1
        return inputs

    def run_program(self, inputs):
        self.variables = variables = {
            'x': 0,
            'y': 0,
            'z': 0,
            'w': 0,
        }
        inputs = iter(inputs)
        def do_op(op, params):
            var = params[0]
            assert var in variables
            val = params[1]
            if val in variables:
                val = variables[val]

            variables[var] = op(variables[var], val)

        def eq(x, y):
            return int(x == y)

        for name, params in self.instructions:
            if name == "inp":
                param = params[0]
                variables[param] = next(inputs)
            elif name == "add":
                do_op(operator.add, params)
            elif name == "mul":
                do_op(operator.mul, params)
            elif name == "div":
                do_op(operator.floordiv, params)
            elif name == "mod":
                do_op(operator.mod, params)
            elif name == "eql":
                do_op(eq, params)


def manual_imp(inputs):
    x = 0
    y = 0
    z = 0
    w = 0

    # 1
    w = inputs[0]
    x = 1
    y = inputs[0] + 2
    z = y

    # z [d0 + 2] base 26

    # 2
    w = inputs[1]
    x = 1
    y = inputs[1] + 4
    z = 26*z + y
    # z is [d0+2, d1+4] base 26

    # 3
    w = inputs[2]
    x = 1
    y = inputs[2] + 8
    z = 26*z + y

    # z is [d0+2, d1+4, d2+8] base 26

    # 4
    w = inputs[3]
    x = 1
    y = inputs[3] + 7
    z = 26*z + y

    # z is [d0+2, d1+4, d2+8, d3+7] base 26

    # 5
    w = inputs[4]
    x = 1
    y = inputs[4] + 12
    z = 26*z + y

    # z is [d0+2, d1+4, d2+8, d3+7, d4+12] base 26

    # 6
    w = inputs[5]
    x = z % 26
    z //= 26    # z is now [d0+2, d1+4, d2+8, d3+7] base 26
    if x - 14 == w:
        x = 0
        y = 0
    else:
        print("d5 wrong")
        x = 1
        y = inputs[5] + 7
        z = z*26 + y

    # 7
    w = inputs[6]
    x = z % 26
    z //= 26
    if x == w:
        x = 0
        y = 0
    else:
        print("d6 wrong")
        x = 1
        y = inputs[6] + 10
        z = z*26 + y

    # 8
    w = inputs[7]
    x = 1
    y = inputs[7] + 14
    z = z*26 + y

    # 9
    w = inputs[8]
    x = z % 26
    z //= 26
    if x - 10 == w:
        x = 0
        y = 0
    else:
        print("d8 wrong")
        x = 1
        y = inputs[8] + 2
        z = 26*z + y

    # 10
    w = inputs[9]
    x = 1
    y = inputs[9] + 6
    z = z*26 + y

    # 11
    w = inputs[10]
    x = z % 26
    z //= 26
    if x - 12 == w:
        x = 0
        y = 0
    else:
        print("d10 wrong")
        x = 1
        y = inputs[10] + 8
        z = 26*z + y

    # 12
    w = inputs[11]
    x = z % 26
    z //= 26
    if x - 3 == w:
        x = 0
        y = 0
    else:
        print("d11 wrong", inputs[11], x)
        x = 1
        y = inputs[11] + 11
        z = 26*z + y

    # 13
    w = inputs[12]
    x = z % 26
    z //= 26
    if x - 11 == w:
        x = 0
        y = 0
    else:
        x = 1
        y = inputs[12] + 5
        z = 26*z + y

    # 14
    w = inputs[12]
    x = z % 26
    z //= 26
    if x - 2 == w:
        x = 0
        y = 0
    else:
        x = 1
        y = inputs[12] + 11
        z = 26*z + y

    return (x, y, z, w)



def part_1(data):
    # 2:14:37
    # part 2: 2:17:19
    parser = Parser(data)
    for inputs in [list(map(int, "18113181571611"))]:
        try:
            parser.run_program(inputs)
        except StopIteration:
            v = parser.variables
            output = (v['x'], v['y'], v['z'], v['w'])
            if output == manual_imp(inputs):
                print(inputs, output, manual_imp(inputs))
        else:
            print(parser.variables)
            print(manual_imp(inputs))


def main():
    data = open("input.txt").read().strip()
    lines = data.splitlines()
    print(part_1(lines))



if __name__ == "__main__":
    main()
