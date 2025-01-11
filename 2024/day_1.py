import os


def load_data(file):
    with open(f'input/{file}.txt') as f:
        data = f.read().split('\n')
        left = []
        right = []
        for line in data:
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
        return left, right


def solve_part_1():
    left, right = load_data("day_1")

    total = 0
    for l, r in zip(sorted(left), sorted(right)):
        total += (abs(l - r))
    return total


def solve_part_2():
    left, right = load_data("day_1")

    right_count = {}
    for value in right:
        if value in right_count:
            right_count[value] += 1
        else:
            right_count[value] = 1

    similarity_score = 0
    for value in left:
        similarity_score += value * right_count.get(value, 0)

    return similarity_score


print(solve_part_1())
print(solve_part_2())