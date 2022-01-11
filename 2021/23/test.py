from collections import Counter


class Puzzle:
    amphipod_types = {
        'A': "Amber",
        'B': "Bronze",
        'C': "Copper",
        'D': "Desert",
    }

    amphipod_energies = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }

    def __init__(self, initial_layout):
        self.grid = initial_layout
        self.walkable = self.initialise_walkable_areas()
        self.rooms = self.initialise_rooms()
        self.outside_rooms = self.initialise_outside_rooms()
        self.rest_squares = self.initialise_rest_squares()

    def initialise_walkable_areas(self):
        paths = []
        for row_num, row in enumerate(self.grid):
            for col_num, char in enumerate(row):
                if char == '.' or char in self.amphipod_types:
                    paths.append((row_num, col_num))
        return tuple(paths)


    def initialise_rooms(self):
        room_tiles = []
        for row_num, row in enumerate(self.grid):
            for col_num, char in enumerate(row):
                if char in self.amphipod_types:
                    room_tiles.append((row_num, col_num))

        columns = sorted(set(pos[1] for pos in room_tiles))
        self.room_columns = tuple(columns)

        assert len(columns) == len(self.amphipod_types)

        rooms = {}
        for amphipod, col_num in zip(self.amphipod_types, columns):
            rooms[amphipod] = sorted(x for x in room_tiles if x[1] == col_num)

        return rooms

    def initialise_outside_rooms(self):
        outside_rooms = []
        for row_num, row in enumerate(self.grid):
            for col_num, char in enumerate(row):
                if col_num in self.room_columns and char == '.':
                    outside_rooms.append((row_num, col_num))

        self.corridor_row = outside_rooms[0][0]

        return outside_rooms

    def initialise_rest_squares(self):
        restable = []
        for row, col in self.walkable:
            if col not in self.room_columns:
                restable.append((row, col))
        return restable


    def legal_moves(self, layout):
        amphipods = []
        for row, col in self.walkable:
            square = layout[row][col]
            if square in self.amphipod_types:
                amphipods.append((square, (row, col)))

        # For each amphipod, we first work out what squares are free for them
        # to walk to without crashing into another amphipod.

        for item in amphipods:
            amphipod, pos = item
            targets = {}
            to_visit = [pos]
            while to_visit:
                square = to_visit.pop(0)
                energy = (
                    targets.get(square, 0) + self.amphipod_energies[amphipod]
                )
                for nbour in self.neighbours(*square):
                    if layout[nbour[0]][nbour[1]] != '.':
                        # Can't walk here! Something in the way.
                        continue
                    if nbour in targets:
                        # Already got this one. Skip it.
                        continue
                    to_visit.append(nbour)
                    targets[nbour] = energy
            # Targets now contain squares which can be walked to by the
            # amphipod. We now need to filter them by the rules.

            # First, we cannot stop outside a room:
            for square in self.outside_rooms:
                targets.pop(square, None)

            # If the destination is a room, it must be the room for this
            # amphipod, and the room must not contain any other types of
            # amphipod
            invalid_targets = []
            for square in targets:
                for room, tiles in self.rooms.items():
                    if square not in tiles:
                        continue

                    if room != amphipod:
                        invalid_targets.append(square)
                    else:
                        other_amphipods = False
                        for row, col in tiles:
                            if layout[row][col] not in (".", amphipod, "H"):
                                other_amphipods = True
                        if other_amphipods:
                            invalid_targets.append(square)

            for square in invalid_targets:
                targets.pop(square)

            # If they are initially in the corridor, then they MUST move into
            # a room.

            in_hall = True
            for tiles in self.rooms.values():
                if pos in tiles:
                    in_hall = False

            if in_hall:
                # Remove any target square that isn't in a room
                invalid_targets = []
                for square in targets:
                    in_hall = True
                    for tiles in self.rooms.values():
                        if square in tiles:
                            in_hall = False
                    if in_hall:
                        invalid_targets.append(square)
                for square in invalid_targets:
                    targets.pop(square)

            # For efficiency, there is never any point in moving an amphipod
            # to its room, if it isn't the deepest possible room allowed.
            room_targets = []
            for square in targets:
                if square in self.rooms[amphipod]:
                    room_targets.append(square)
            if len(room_targets) == 2:
                # Remove the room that is highest
                targets.pop(min(room_targets))

            for target, cost in targets.items():
                yield (pos, target, cost)

    def lower_bound_energy(self, layout):
        # Compute a lower bound of energy required for a given position to get
        # every amphipod back home.

        # First find all the amphipods

        amphipods = []
        for row, col in self.walkable:
            if layout[row][col] in self.amphipod_types:
                amphipods.append((row, col))

        minimum_energy = 0

        # How many amphipods have we sent home of a given type? Each one
        # requires one more step than the last to get into it's room.
        amphipods_home = Counter()
        for amphipod_pos in amphipods:
            row, col = amphipod_pos
            amphipod = layout[row][col]
            # Is it already home?
            if amphipod_pos in self.rooms[amphipod]:
                # No energy required here
                print(amphipod, amphipod_pos, "already home")
                continue
            amphipods_home[amphipod] += 1

            # Is it in another room?
            for room, tiles in self.rooms.items():
                if room == amphipod:
                    continue
                else:
                    if amphipod_pos in tiles:
                        print(amphipod, amphipod_pos, "in wrong room")
                        # We need to travel out of this room by going up
                        steps = amphipod_pos[0] - self.corridor_row
                        # We need to move to the correct column
                        col = self.rooms[amphipod][0][1]
                        steps += abs(col - amphipod_pos[1])
                        # Add remaining steps to get into correct room
                        steps += amphipods_home[amphipod]
                        minimum_energy += (
                            steps * self.amphipod_energies[amphipod]
                        )
                        print("{} steps to get it home!".format(steps))
                        break
            else:
                # Otherwise we are in the corridor
                # Add steps to get into correct room:
                steps = amphipods_home[amphipod]
                col = self.rooms[amphipod][0][1]
                steps += abs(col - amphipod_pos[1])
                minimum_energy += steps * self.amphipod_energies[amphipod]

        return minimum_energy



    def neighbours(self, row, col):
        for index in range(2):
            for diff in (-1, 1):
                nbour = [row, col]
                nbour[index] += diff
                nbour = tuple(nbour)
                if nbour in self.walkable:
                    yield nbour

    def everyone_home(self, layout):
        for row_num, col_num in self.walkable:
            char = layout[row_num][col_num]
            if char not in '.H':
                if (row_num, col_num) not in self.rooms[char]:
                    return False
        return True

    def optimal_solution(self, layout, running_cost=0, depth=0):
        if depth == 0:
            self.best_solution = float('inf')

        if running_cost + self.lower_bound_energy(layout) >= self.best_solution:
            # No point continuing! No improvement to be made here
            return None

        if self.everyone_home(layout):
            if running_cost < self.best_solution:
                self.best_solution = running_cost
                print(running_cost)
            return running_cost

        costs = []
        if depth == 1:
            print(list(self.legal_moves(layout)))
            self.print_layout(layout)

        for start, end, cost in self.legal_moves(layout):
            if depth == 0:
                print(costs)
            elif depth == 1:
                print("\t", costs)
            new_layout = self.move(layout, start, end)
            sol = self.optimal_solution(
                new_layout,
                running_cost + cost,
                depth+1
            )
            if sol is not None:
                costs.append(sol)
        if costs:
            return min(costs)
        else:
            return None

    def print_layout(self, layout):
        for row in layout:
            print("".join(row))

    def move(self, layout, start, end):
        copy = [list(line) for line in layout]
        start_tile = layout[start[0]][start[1]]
        end_tile = layout[end[0]][end[1]]

        # If we are moving something into its room, replace it with H so it
        # can't move again.

        if end in self.rooms[start_tile]:
            start_tile = "H"

        copy[start[0]][start[1]] = end_tile
        copy[end[0]][end[1]] = start_tile

        return copy



def part_1(puz):
    return puz.optimal_solution(puz.grid)


def main():
    data = open("input.txt").read().strip()
    lines = data.splitlines()

    layout = """#############
#...........#
###A#C#B#B###
  #D#C#B#A#
  #D#B#A#C#
  #D#D#A#C#
  #########""".splitlines()
    puz = Puzzle(layout)
    print(puz.lower_bound_energy(layout))


if __name__ == "__main__":
    main()
