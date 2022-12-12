#!/usr/bin/env python3.10

# 39:05
# 46:50

import re

def get_input():
    text = open("input.txt").read().rstrip()
    return text


class Monkeys:
    def __init__(self, monkey_data):
        self.parse_data(monkey_data)


    def parse_data(self, data):
        self.monkeys = monkeys = {}
        for block in data.split("\n\n"):
            lines = block.splitlines()
            line0 = lines[0]
            monkey_num = int(re.match("Monkey (\d+)", line0).groups()[0])
            monkey = {
                'number': monkey_num,
                'inspected': 0
            }
            monkeys[monkey_num] = monkey

            starting_items = lines[1].strip()
            starting_items = starting_items.split(":")[1]
            item_nums = list(map(int, starting_items.split(",")))
            monkey["starting_items"] = item_nums
            monkey["current_items"] = list(item_nums)

            operation = lines[2].split(":")[1].strip()
            monkey["operation"] = self.parse_operation(operation)

            test = lines[3].split(":")[1]

            monkey["test"] = self.parse_test(test)

            if_true = lines[4].strip()
            if_true = int(
                re.match("If true: throw to monkey (\d+)", if_true).groups()[0]
            )
            if_false = lines[5].strip()
            if_false = int(re.match(
                "If false: throw to monkey (\d+)", if_false
            ).groups()[0])

            monkey['if_true'] = if_true
            monkey['if_false'] = if_false

    def parse_operation(self, op_string):
        lhs, rhs = op_string.split("=")
        assert lhs.strip() == "new"
        rhs = rhs.strip()

        if "*" in rhs:
            t1, t2 = rhs.split("*")
            return lambda x: self.term(t1)(x) * self.term(t2)(x)

        elif "+" in rhs:
            t1, t2 = rhs.split("+")
            return lambda x: self.term(t1)(x) + self.term(t2)(x)

    def term(self, term_string):
        term_string = term_string.strip()
        if term_string == "old":
            return lambda x: x
        else:
            return lambda x: int(term_string)

    def parse_test(self, test_string):
        test_string = test_string.strip()
        val = int(re.match("divisible by (\d+)", test_string).groups()[0])
        return lambda x: (x % val) == 0

    def perform_round(self):
        for monkey_num in sorted(self.monkeys.keys()):
            monkey = self.monkeys[monkey_num]
            self.take_turn(monkey)

    def take_turn(self, monkey):
        new_current_items = []
        for item in monkey['current_items']:
            worry_level = item
            worry_level = monkey['operation'](worry_level)
            worry_level = self.relief(worry_level)
            if monkey['test'](worry_level):
                throw_to = monkey['if_true']
            else:
                throw_to = monkey['if_false']

            if throw_to != monkey['number']:
                self.monkeys[throw_to]['current_items'].append(worry_level)
            else:
                new_current_items.append(worry_level)

            monkey['inspected'] += 1

        monkey['current_items'] = new_current_items

    def relief(self, worry):
        return worry // 3


class Part2(Monkeys):
    def __init__(self, *args, **kwargs):
        self.divisibility_vals = []
        super().__init__(*args, **kwargs)
        self.get_modulo()

    def get_modulo(self):
        self.modulo = 1
        for factor in self.divisibility_vals:
            if self.modulo % factor != 0:
                self.modulo *= factor

    def parse_operation(self, op_string):
        operation = super().parse_operation(op_string)
        return lambda x: operation(x) % self.modulo

    def relief(self, worry):
        return worry

    def parse_test(self, test_string):
        test_string = test_string.strip()
        val = int(re.match("divisible by (\d+)", test_string).groups()[0])
        self.divisibility_vals.append(val)
        return lambda x: (x % val) == 0



def main():
    text = get_input()
    monkeys = Monkeys(text)

    for __ in range(20):
        monkeys.perform_round()

    inspected = [monkey['inspected'] for monkey in monkeys.monkeys.values()]
    x, y = sorted(inspected, reverse=True)[:2]
    monkey_business = x*y
    print(x*y)


    monkeys = Part2(text)

    for count in range(10000):
        monkeys.perform_round()

    inspected = [monkey['inspected'] for monkey in monkeys.monkeys.values()]
    x, y = sorted(inspected, reverse=True)[:2]
    monkey_business = x*y
    print(x*y)


if __name__ == "__main__":
    main()
