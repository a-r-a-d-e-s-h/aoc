class MatchError(Exception):
    pass


class UnexpectedSymbolError(Exception):
    pass


class Expression:
    extra = ""
    def __init__(self, data):
        self.data = data
        self.position = 0

    def parse(self):
        output = []
        while 1:
            pos = self.position
            for Expr in [Paren, Square, Curly, Angled]:
                try:
                    output.append(self.match(Expr))
                except MatchError:
                    self.position = pos
                else:
                    break
            else:
                return "".join(output)

    def match_char(self, char):
        try:
            next_char = self.data[self.position]
        except IndexError:
            raise MatchError

        if next_char != char:
            raise MatchError
        self.position += 1
        return char

    def match_char_or_fill(self, char):
        if self.position == len(self.data):
            self.data += char
            self.extra += char
        return self.match_char(char)

    def match(self, grammar_type):
        expr = grammar_type(self.data[self.position:])
        output = expr.parse()
        self.data += expr.extra
        self.extra += expr.extra
        self.position += len(output)
        return output


class BracketType(Expression):
    open_symb = None
    close_symb = None
    def parse(self):
        output = ""
        output += self.match_char(self.open_symb)
        output += self.match(Expression)
        if self.position > len(self.data):
            raise Exception("", self.extra)
        try:
            output += self.match_char_or_fill(self.close_symb)
        except MatchError:
            raise UnexpectedSymbolError(self.data[self.position])

        return output


class Paren(BracketType):
    open_symb = "("
    close_symb = ")"


class Square(BracketType):
    open_symb = "["
    close_symb = "]"


class Curly(BracketType):
    open_symb = "{"
    close_symb = "}"


class Angled(BracketType):
    open_symb = "<"
    close_symb = ">"


def parse_line(line):
    expr = Expression(line)
    output = expr.parse()
    if output == line:
        return line


def part_1(data):
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    score = 0

    for line in data:
        try:
            parse_line(line)
        except UnexpectedSymbolError as e:
            symb = e.args[0]
            score += scores[symb]

    return score

def part_2(data):
    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    line_scores = []
    for line in data:
        try:
            expr = Expression(line)
            output = expr.parse()
            line_score = 0
            for char in expr.extra:
                line_score *= 5
                line_score += scores[char]
            line_scores.append(line_score)
        except UnexpectedSymbolError:
            pass

    line_scores.sort()

    return line_scores[len(line_scores)//2]


def main():
    data = open("input.txt").read().strip().splitlines()

    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
