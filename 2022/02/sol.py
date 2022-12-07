# 10:35
# 16:26

def get_input():
    text = open("input.txt").read()
    return text.splitlines()


def main():
    data = get_input()

    rounds = [x.split() for x in data]

    maps = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
        "X": "rock",
        "Y": "paper",
        "Z": "scissors",
    }

    scores = {
        "rock": 1,
        "paper": 2,
        "scissors": 3,
    }

    total_score = 0

    loss = 0
    draw = 3
    win = 6

    def calculate_score(choice_1, choice_2):
        round_score = scores[choice_2]

        if choice_1 == choice_2:
            round_score += draw
        else:
            if (choice_1, choice_2) in (
                ("rock", "scissors"),
                ("scissors", "paper"),
                ("paper", "rock"),
            ):
                round_score += loss
            else:
                round_score += win
        return round_score

    for player_1, player_2 in rounds:
        choice_1 = maps[player_1]
        choice_2 = maps[player_2]

        total_score += calculate_score(choice_1, choice_2)

    print(total_score)

    # part 2
    strategy = {
        "X": "lose",
        "Y": "draw",
        "Z": "win",
    }

    total_score = 0
    for player_1, player_2 in rounds:
        choice_1 = maps[player_1]
        outcome = strategy[player_2]
        if outcome == "draw":
            choice_2 = choice_1
        elif outcome == "win":
            choice_2 = {
                "rock": "paper",
                "scissors": "rock",
                "paper": "scissors",
            }[choice_1]
        elif outcome == "lose":
            choice_2 = {
                "paper": "rock",
                "rock": "scissors",
                "scissors": "paper",
            }[choice_1]

        total_score += calculate_score(choice_1, choice_2)

    print(total_score)




if __name__ == "__main__":
    main()
