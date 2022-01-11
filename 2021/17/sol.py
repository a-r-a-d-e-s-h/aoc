import re
from itertools import count


def part_1(x, y):
    # 46:56

    y_min, y_max = y
    # For a velocity v, the highest point reached will be v(v+1)/2, so we must
    # maximise v.
    # For a velocity v, the position at step n will be:
    # nv - n(n-1)/2

    # If this value lies in our range for some n then we require
    # (v+1/2)^2 + 2a
    # to be of the form (m+1/2)^2 for some integer m with y_min <= a <= y_max
    # i.e. v(v+1)/2 + a = m(m+1)/2
    # the largest v where this is possible will be such that:
    # v(v+1)/2 + a = v(v-1)/2
    # because a is negative
    # so v + a = 0
    # So v = -y_min

    return y_min*(y_min + 1)//2


def part_2(x, y):
    # 84:45

    # From part 1 we know the maximum y-velocity we can use. Also we know the
    # minimum y-velocity we can use, as it will simply be y_min. So for each
    # y-velocity, we can work out what x-velocities will also work
    y_min, y_max = y
    x_min, x_max = x

    total_choices = 0

    for y_v in range(y_min, -y_min + 1):
        # First compute what steps we are in the y-range
        y_pos = 0
        valid_steps = []
        for step in count(start=1):
            y_pos += y_v - (step - 1)
            if y_min <= y_pos <= y_max:
                valid_steps.append(step)

            if y_pos < y_min:
                break
        x_vs = set()
        for step in valid_steps:
            # Find x velocities which place us in the right x range on this
            # step
            # Max possible will always be x_max:
            for x_v in range(x_max + 1):
                x_pos = 0
                for i in range(step):
                    x_pos += max(x_v - i, 0)
                if x_min <= x_pos <= x_max:
                    x_vs.add(x_v)
        total_choices += len(x_vs)
    return total_choices



def main():
    data = open("input.txt").read().strip()
    res = list(map(int, re.findall("-?\d+", data)))
    x = res[:2]
    y = res[2:]
    print(part_1(x, y))
    print(part_2(x, y))


if __name__ == "__main__":
    main()
