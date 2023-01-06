from itertools import zip_longest
from functools import cmp_to_key


def load_data(file):
    with open(f"input/{file}.txt") as f:
        data = f.read().split('\n\n')
        data = [d.split('\n') for d in data]
        return data


def parse_nested_list(string):
    result, _i = parse_list(string)
    return result


def parse_list(string, i=0):
    result = []
    first_parens = True
    current_number = ''

    while i < len(string):
        char = string[i]

        match char:
            case '[':
                if first_parens:
                    first_parens = False
                    i += 1
                else:
                    sublist, i = parse_list(string, i)
                    result.append(sublist)
            case ',':
                if current_number:
                    result.append(int(current_number))
                current_number = ''
                i += 1
            case ']':
                if current_number:
                    result.append(int(current_number))
                current_number = ''
                return result, i + 1
            case number_char:
                current_number += number_char
                i += 1


def check_order(left, right):
    for l, r in zip_longest(left, right):
        is_ordered = None
        if type(l) == int and type(r) == int:
            if l < r:
                return True
            elif l > r:
                return False
        elif type(l) == list and type(r) == list:
            is_ordered = check_order(l, r)

        elif type(l) == list and type(r) == int:
            is_ordered = check_order(l, [r])

        elif type(l) == int and type(r) == list:
            is_ordered = check_order([l], r)

        elif l == None:
            return True
        elif r == None:
            return False

        if is_ordered != None:
            return is_ordered


def comparison_function(left, right):
    mapping = {None: 0, True: 1, False: -1}
    return mapping[check_order(left, right)]


if __name__ == "__main__":
    data = load_data("day_13")

    pairs = []
    for left, right in data:
        pairs.append((parse_nested_list(left), parse_nested_list(right)))

    correct_indices = []
    for (i, (left, right)) in enumerate(pairs):
        index = i + 1
        if result := check_order(left, right):
            correct_indices.append(index)

    print(f'Part 1: sum of indices of correct pairs = {sum(correct_indices)}')

    all_signals = [first_divider := [[2]], second_divider := [[6]]]
    for pair in pairs:
        for signal in pair:
            all_signals.append(signal)

    sorted_signals = sorted(all_signals, key=cmp_to_key(comparison_function))

    for i, signal in enumerate(sorted_signals):
        index = i + 1
        if signal == first_divider:
            divider_index_1 = index
        if signal == second_divider:
            divider_index_2 = index

    decoder_key = divider_index_1 * divider_index_2

    print(f'Part 2: decoder key is: {decoder_key}')
