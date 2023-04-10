def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read().split('\n')


class MathMonkey:
    def __init__(self, id, upstream_1, operator, upstream_2):
        self.id = id
        self.upstream_1 = upstream_1
        self.upstream_2 = upstream_2
        self.operator = operator

    def __repr__(self):
        return f'({self.id}: {self.upstream_1} {self.operator} {self.upstream_2})'


def parse_data(data):
    number_monkeys = {}
    math_monkeys = {}

    for record in data:
        left, right = record.split(':')
        right = right.strip()
        if len(right) < 7:
            number_monkeys[left] = int(right)
        else:
            monkey = MathMonkey(left, *right.split(' '))
            math_monkeys[left] = monkey

    return number_monkeys, math_monkeys


def solve_1(monkey, number_monkeys, math_monkeys):
    if monkey in number_monkeys:
        return number_monkeys[monkey]

    mm = math_monkeys[monkey]

    upstream_1 = solve_1(mm.upstream_1, number_monkeys, math_monkeys)
    upstream_2 = solve_1(mm.upstream_2, number_monkeys, math_monkeys)

    match mm.operator:
        case '+':
            return upstream_1 + upstream_2
        case '-':
            return upstream_1 - upstream_2
        case '*':
            return upstream_1 * upstream_2
        case '/':
            return int(upstream_1 / upstream_2)


if __name__ == '__main__':
    data = load_data('day_21')
    number_monkeys, math_monkeys = parse_data(data)

    result = solve_1("root", number_monkeys, math_monkeys)
    print(f'Part 1 solution: {result}')
