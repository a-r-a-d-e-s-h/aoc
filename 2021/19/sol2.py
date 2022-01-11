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

    # Let's re-orientate and translate each sensor's data to align with sensor
    # 0.

    aligned = {0: data[0]}
    transform_maps = {0: TransformMap.identity}

    remaining = [key for key in data if key not in aligned]

    while remaining:
        found_pair = False
        for s1 in remaining:
            for s0 in aligned:
                T = find_transform_map(aligned[s0], data[s1])
                if T is not None:
                    aligned[s1] = [T(pt) for pt in data[s1]]
                    transform_maps[s1] = T
                    remaining.remove(s1)
                    found_pair = True
                    break


    all_beacons = Counter()
    for key in aligned:
        s = aligned[key]
        for pt in s:
            all_beacons[tuple(pt)] = 1

    print(sum(all_beacons.values()))

    max_dist = 0

    for t0, t1 in combinations(transform_maps.values(), r=2):
        dist = sum(map(abs, t0.shift - t1.shift))
        max_dist = max(dist, max_dist)

    print(max_dist)



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
