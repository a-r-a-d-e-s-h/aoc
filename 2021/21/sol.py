from functools import cache


def part_1(p1_pos, p2_pos):
    p1_score = 0
    p2_score = 0

    def dice():
        while 1:
            for i in range(1, 101):
                yield i

    d = dice()

    scores = [0, 0]
    positions = [p1_pos, p2_pos]

    rolls = 0
    player = 0
    while 1:
        score = sum([next(d) for __ in range(3)])
        rolls += 3
        new_pos = (positions[player] + score - 1)%10 + 1
        positions[player] = new_pos
        scores[player] += new_pos
        if scores[player] >= 1000:
            return scores[(player + 1)%2] * rolls
        player = (player + 1)%2


def part_2(p1_pos, p2_pos):
    start_pos = [p1_pos, p2_pos]

    @cache
    def universe_count(positions, scores):
        """
        Given the current scores and the positions, compute how many
        universes players 1 and 2 win in respectively. It is player 1's turn.
        """
        goal = 21
        if scores[0] >= goal:
            return (1, 0)
        elif scores[1] >= goal:
            return (0, 1)

        # We roll:
        # 1 + 1 + 1 = 3 (in 1 universe)
        # 1 + 1 + 2 = 4 (in 3 universes)
        # 1 + 2 + 2 = 1 + 1 + 3 = 5 (in 6 universes)
        # 1 + 2 + 3 = 2 + 2 + 2 = 6 (in 7 universes)
        # 1 + 3 + 3 = 2 + 2 + 3 = 7 (in 6 universes)
        # 2 + 3 + 3 = 8 (in 3 universes)
        # 3 + 3 + 3 = 9 (in 1 universe)

        count_multipliers = (
            (3, 1),
            (4, 3),
            (5, 6),
            (6, 7),
            (7, 6),
            (8, 3),
            (9, 1),
        )

        ways_to_win = [0, 0]
        for score, multiplier in count_multipliers:
            new_pos = (positions[0] + score - 1)%10 + 1
            counts = universe_count(
                (positions[1], new_pos), (scores[1], scores[0] + new_pos)
            )
            ways_to_win[0] += multiplier * counts[1]
            ways_to_win[1] += multiplier * counts[0]
        return tuple(ways_to_win)

    return max(universe_count((p1_pos, p2_pos), (0, 0)))






def main():
    data = open("input.txt").read().strip()
    lines = data.splitlines()
    p1 = int(lines[0].split(":")[1])
    p2 = int(lines[1].split(":")[1])
    print(part_1(p1, p2))
    print(part_2(p1, p2))


if __name__ == "__main__":
    main()
