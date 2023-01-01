import time

def load_data():
    with open("input/day_11.txt") as f:
        return f.read().split('\n\n')

class Monkey:
    def __init__(self, input):
        lines = [line.strip() for line in input.split('\n')]
        self.id = int(lines[0].split(' ')[1].replace(':',''))
        self.items = [int(item) for item in lines[1].replace('Starting items: ', '')
                                                    .replace(',', '')
                                                    .split(' ')]
        operation = lines[2].replace("Operation: new = old ", "").split(' ')
        self.operation = operation[0]
        self.operation_constant = operation[1]                                                    
        self.divisor = int(lines[3].replace("Test: divisible by ", ""))
        self.destination_true = int(lines[4].replace("If true: throw to monkey ", ""))
        self.destination_false = int(lines[5].replace("If false: throw to monkey ", ""))
        self.inspection_count = 0

    def play_turn(self):
        for item in self.items:
            self.inspection_count += 1
            item = self.inspect(item)
            self.throw(item)
        self.items = []
    
    def inspect(self, item):
        if self.operation_constant == 'old':
            constant = item
        else:
            constant = int(self.operation_constant)

        if self.operation == '*':
            worry = item * constant
        elif self.operation == '+':
            worry = item + constant

        if part == 1:
            worry = worry//3
        else:
            worry = worry % worry_reducer
       
        return worry

    def throw(self, item):
        if self.test(item):
            monkeys[self.destination_true].catch(item)
        else:
            monkeys[self.destination_false].catch(item)

    def test(self, item):    
        return item % self.divisor == 0

    def catch(self, item):
        self.items.append(item)

    def __repr__(self):
        return f"""Monkey: {self.id}
    Items: {self.items}
    Inspections: {self.inspection_count}
    Operation: {self.operation}= {self.operation_constant}
    Test: divisible by {self.divisor}
        true: {self.destination_true}
        false: {self.destination_false}
    """

def top_two(numbers):
    copied_numbers = numbers.copy()
    first = max(copied_numbers)
    copied_numbers.remove(first)
    second = max(copied_numbers)
    return first, second

if __name__ == "__main__":
    raw_monkeys_texts = load_data()

    part = 1

    monkeys = [Monkey(monkey_text) for monkey_text in raw_monkeys_texts]

    divisors = [monkey.divisor for monkey in monkeys]
    worry_reducer = 1
    for d in divisors:
        worry_reducer *= d

    for _round in range(20):
        for monkey in monkeys:
            monkey.play_turn()

    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    first, second = top_two(inspection_counts)
    print(f"Result Part 1: {first*second}") 

    part = 2
    monkeys = [Monkey(monkey_text) for monkey_text in raw_monkeys_texts]    
    for round in range(10000):
        for monkey in monkeys:
            monkey.play_turn()

    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    first, second = top_two(inspection_counts)
    print(f"Result Part 2: {first*second}") 


