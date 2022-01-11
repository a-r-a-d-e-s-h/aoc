from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import numpy as np
import re


def generate_rotations():
    # All the rotations we want are those with +/-1 with exactly one in each
    # row/column and determinant +1
    all_rots = []

    for perm in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            arr = np.zeros((3, 3), dtype=int)
            for i in range(3):
                arr[i, perm[i]] = signs[i]
            if np.linalg.det(arr) == 1:
                all_rots.append(arr)
    return all_rots


all_rotations = generate_rotations()


class TransformMap:
    def __init__(self, rot, shift):
        self.rot = rot
        self.shift = shift

    def __call__(self, vec):
        return self.rot.dot(vec) + self.shift

    def inverse(self):
        rot = self.rot
        shift = self.shift
        rot_inv = np.linalg.inv(rot)
        rot_inv = np.array(rot_inv, dtype=int)
        return TransformMap(rot_inv, -rot_inv.dot(shift))

    def compose(self, T):
        return TransformMap(
            self.rot.dot(T.rot), self.rot.dot(T.shift) + self.shift
        )

    @classmethod
    @property
    def identity(cls):
        return cls(np.identity(3, dtype=int), np.zeros(3, dtype=int))


def find_translation(s0, s1, overlap=12):
    # Given two collection of points s0, s1, see if we  can find a translation
    # vector T such that s0 = s1 + T has at least overlap common points.
    shifts = Counter()
    for v0, v1 in product(s0, s1):
        diff = tuple(v0 - v1)
        shifts[diff] += 1
        if shifts[diff] >= overlap:
            return v0 - v1


def find_transform_map(s0, s1, overlap=12):
    for rot in all_rotations:
        s1_rotated = [rot.dot(s) for s in s1]
        translation = find_translation(s0, s1_rotated, overlap=overlap)
        if translation is not None:
            return TransformMap(rot, translation)
    return None


def part_1(data):
    # 1:56:42

    # Create a collection of tuples (s0, s1, T) where s0, s1 are sensors and
    # T is a transform such that s0 = T(s1)
    # In fact we will keep them is dictionaries of the form:
    #   s0: [(s1, T), ...]

    connections = defaultdict(list)

    for s0, s1 in combinations(data, r=2):
        T = find_transform_map(data[s0], data[s1])
        if T is not None:
            connections[s0].append((s1, T))
            connections[s1].append((s0, T.inverse()))

    maps_to_zero = {}
    maps_to_zero[0] = TransformMap.identity
    remaining = [key for key in data if key != 0]
    while remaining:
        for key in list(maps_to_zero.keys()):
            for s1, T in connections[key]:
                if s1 in remaining:
                    maps_to_zero[s1] = maps_to_zero[key].compose(T)
                    remaining.remove(s1)

    all_beacons = set()
    for s in data:
        transform = maps_to_zero[s]
        for pt in data[s]:
            all_beacons.add(tuple(transform(pt)))
    
    print(len(all_beacons))

    scanner_positions = []
    for __, T in maps_to_zero.items():
        scanner_positions.append(T.shift)

    max_diff = 0
    for p0, p1 in combinations(scanner_positions, r=2):
        diff = tuple(p0 - p1)
        max_diff = max(max_diff, sum(map(abs, diff)))

    # 2:04:30
    print(max_diff)


def main():
    data = open("input.txt").read().strip()

    sections = data.split('\n\n')

    scanner_data = {}
    for section in sections:
        section = section.splitlines()
        header = section[0]
        num = int(re.search("-?\d+", header).group())
        scanner_data[num] = [
            np.array(list(map(int, line.split(',')))) for line in section[1:]
        ]
    part_1(scanner_data)



if __name__ == "__main__":
    main()
