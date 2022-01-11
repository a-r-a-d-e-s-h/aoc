from collections import Counter, namedtuple
from itertools import product
import re


class Cuboid:
    def __init__(self, x_range, y_range, z_range):
        for pair in (x_range, y_range, z_range):
            assert len(pair) == 2
            assert pair[0] <= pair[1]
        self.x_range = tuple(x_range)
        self.y_range = tuple(y_range)
        self.z_range = tuple(z_range)

    def volume(self):
        return self.x_len * self.y_len * self.z_len

    @property
    def x_len(self):
        return self.x_range[1] - self.x_range[0] + 1

    @property
    def y_len(self):
        return self.y_range[1] - self.y_range[0] + 1

    @property
    def z_len(self):
        return self.z_range[1] - self.z_range[0] + 1

    def minus(self, cuboid):
        # Yields disjoint cubes equaling to self \ cuboid
        cuboid = self.intersect(cuboid)
        if cuboid is None:  # There is no intersection.
            yield self
            return None

        # Can just do self \ (self intersect cuboid)
        # Split into several cuboids, one of them is the intersect, and yield
        # all but that one.
        def split_ranges(x, y):
            a, b = x
            c, d = y
            # [a, b] is an interval of integers and so is [c, d]
            # We have a <= c <= d <= b.
            # We yield the ranges of [a, b] \ [c, d]
            # which might be nothing, a single interval, or two intervals.
            # We also yield the range (c, d)
            assert a <= c <= d <= b

            if a < c:
                yield (a, c - 1)

            yield (c, d)

            if d < b:
                yield (d + 1, b)

        for x_range in split_ranges(self.x_range, cuboid.x_range):
            for y_range in split_ranges(self.y_range, cuboid.y_range):
                for z_range in split_ranges(self.z_range, cuboid.z_range):
                    new_cub = Cuboid(x_range, y_range, z_range)
                    if new_cub != cuboid:
                        yield new_cub


    def intersect(self, cuboid):
        x_range = (
            max(self.x_range[0], cuboid.x_range[0]),
            min(self.x_range[1], cuboid.x_range[1])
        )
        y_range = (
            max(self.y_range[0], cuboid.y_range[0]),
            min(self.y_range[1], cuboid.y_range[1])
        )
        z_range = (
            max(self.z_range[0], cuboid.z_range[0]),
            min(self.z_range[1], cuboid.z_range[1])
        )
        for r in (x_range, y_range, z_range):
            if r[0] > r[1]:
                return None

        return Cuboid(x_range, y_range, z_range)

    def __eq__(self, rhs):
        return (
            self.x_range == rhs.x_range
            and self.y_range == rhs.y_range
            and self.z_range == rhs.z_range
        )


def part_1(data):
    # 11:52
    space = Counter()

    def in_range(r):
        return r[0] >= -50 and r[1] <= 50 and r[0] <= r[1]

    def our_range(v):
        return range(v[0], v[1] + 1)

    for entry in data:
        if in_range(entry.x) and in_range(entry.y) and in_range(entry.z):
            for x in our_range(entry.x):
                for y in our_range(entry.y):
                    for z in our_range(entry.z):
                        if entry.type == "on":
                            space[x, y, z] = 1
                        else:
                            space[x, y, z] = 0
    return sum(space.values())


def part_2(entries):
    # 88:17
    cuboids = []

    def turn_on(cuboid):
        new_cuboids = [cuboid]
        for cub in cuboids: # For each cuboid already on
            # We replace it with cub \ cuboid
            replace_with = list(cub.minus(cuboid))
            new_cuboids.extend(replace_with)
        cuboids[:] = new_cuboids

    def turn_off(cuboid):
        new_cuboids = []
        for cub in cuboids:
            replace_with = list(cub.minus(cuboid))
            new_cuboids.extend(replace_with)
        cuboids[:] = new_cuboids

    for entry in entries:
        cuboid = Cuboid(entry.x, entry.y, entry.z)
        if entry.type == "on":
            turn_on(cuboid)
        else:
            turn_off(cuboid)

    return sum(cub.volume() for cub in cuboids)


def main():
    data = open("input.txt").read().strip()
    lines = data.splitlines()
    Entry = namedtuple("Entry", ["type", "x", "y", "z"])
    all_items = []
    for line in lines:
        on_off, remaining = line.split(" ", 1)
        ranges = remaining.split(",")
        range_dict = {}
        for entry in ranges:
            variable, r = entry.split("=")
            min_val, max_val = map(int, r.split(".."))
            range_dict[variable] = (min_val, max_val)
        all_items.append(Entry(on_off, **range_dict))

    print(part_1(all_items))
    print(part_2(all_items))


if __name__ == "__main__":
    main()
