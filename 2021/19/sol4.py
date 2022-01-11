from collections import Counter, defaultdict
from functools import cache
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


class ScannerData:
    overlap = 12

    def __init__(self, input_text):
        self.parse_input_text(input_text)

    def parse_input_text(self, text):
        scanner_chunks = text.split("\n\n")
        self.scanner_vectors = {}
        for chunk in scanner_chunks:
            lines = chunk.splitlines()
            number = int(re.search("\d+", lines[0]).group())
            vectors = [
                tuple(map(int, line.split(','))) for line in lines[1:]
            ]
            self.scanner_vectors[number] = vectors

    @property
    def scanners(self):
        yield from sorted(self.scanner_vectors.keys())

    def find_transformation(self, s0, s1):
        # Given scanner indices s0, s1, find a transformation T such that
        # s0 and T(s1) have at least self.overlap points
        s0_pts = self.scanner_vectors[s0]
        s1_rots = self.get_rotated_vectors(s1)
        max_count = 0
        best_transormation = None

        for rot, s1_pts in s1_rots:
            diffs = Counter()
            for v, w in product(s0_pts, s1_pts):
                diff = (v[0] - w[0], v[1] - w[1], v[2] - w[2])
                diffs[diff] += 1
                count = diffs[diff]
                if count > max_count:
                    max_count = count
                    best_transformation = TransformMap(rot, diff)

        if max_count >= self.overlap:
            return best_transformation

    def compute_offsets_for_vector_set(self, vectors):
        offsets = []
        for v in vectors:
            offsets.append((v, set(tuple(-v + pt) for pt in vectors)))
        return offsets

    @cache
    def get_rotated_vectors(self, index):
        # Return list of tuples:
        #   (rot, vectors)
        # where rot is the rotation applied, and vectors is the set of given
        # index with all points rotated by rot.

        rotations = []
        vectors = self.scanner_vectors[index]
        for rot in all_rotations:
            rotated_vectors = [tuple(rot.dot(v)) for v in vectors]
            
            rotations.append((rot, rotated_vectors))
        return rotations


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

        return best_translation


def part_1(data):
    # For each pair of sensors, see if we can map one to the other with a
    # transformation.

    maps = defaultdict(list)

    for s0, s1 in combinations(data.scanners, r=2):
        t_map = data.find_transformation(s0, s1)
        if t_map is not None:
            maps[s0].append((s1, t_map))
            maps[s1].append((s0, t_map.inverse()))

    maps_to_zero = {}
    maps_to_zero[0] = TransformMap.identity
    remaining = [key for key in data.scanner_vectors if key != 0 ]

    while remaining:
        for key in list(maps_to_zero.keys()):
            for s1, t in maps[key]:
                if s1 in remaining:
                    maps_to_zero[s1] = maps_to_zero[key].compose(t)
                    remaining.remove(s1)

    all_beacons = set()
    for s in data.scanners:
        transform = maps_to_zero[s]
        for pt in data.scanner_vectors[s]:
            all_beacons.add(tuple(transform(pt)))

    return len(all_beacons)


def main():
    data = open("input.txt").read().strip()

    sections = data.split('\n\n')

    data = ScannerData(data)
    tot = 0

    print(part_1(data))


if __name__ == "__main__":
    main()
