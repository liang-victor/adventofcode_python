"""--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?"""

def load_data():
    with open("input/day_5.txt") as f:
        raw_data = f.read()
        return raw_data.split("\n\n")

def update_stacks_with_crate_move(stacks, number_of_crates, source, destination):
    updated_source = stacks[source][:-number_of_crates]


    crates_being_moved = stacks[source][-number_of_crates:]    
    updated_destination = stacks[destination] + crates_being_moved[::-1]

    stacks[source] = updated_source
    stacks[destination] = updated_destination
    return stacks

def update_stacks_with_crate_move_9001(stacks, number_of_crates, source, destination):
    updated_source = stacks[source][:-number_of_crates]


    crates_being_moved = stacks[source][-number_of_crates:]    
    updated_destination = stacks[destination] + crates_being_moved

    stacks[source] = updated_source
    stacks[destination] = updated_destination
    return stacks

def set_up_stacks(initial_position_raw):
    position_rows = initial_position_raw.split('\n')[:-1]
    stacks = {(x+1):[] for x in range(9)}

    for row in position_rows[::-1]:
        for x in range(9):
            value = row[(4*x)+1:4*(x+1)-2]
            if value != ' ':
                stacks[x+1].append(value)
    return stacks

def solve():
    [initial_position_raw, moves_raw] = load_data()

    stacks = set_up_stacks(initial_position_raw)

    moves = moves_raw.split("\n")
    moves = [m.split(" ") for m in moves]
    moves = [(int(m[1]), int(m[3]), int(m[5])) for m in moves]

    for (count, source, destination) in moves:
        stacks = update_stacks_with_crate_move(stacks, count, source, destination)


    top_crates = ''
    for stack in stacks.values():
        if stack:
            top_crates += stack[-1]

    print(f'part 1: {top_crates}')

    # part 2
    stacks = set_up_stacks(initial_position_raw)

    
    for (count, source, destination) in moves:
        stacks = update_stacks_with_crate_move_9001(stacks, count, source, destination)


    top_crates = ''
    for stack in stacks.values():
        if stack:
            top_crates += stack[-1]

    print(f'part 2: {top_crates}')

def try_example():
    stacks = {1: ['Z', 'N'],
              2: ['M', 'C', 'D'],
              3: ['P']}
    
    moves = [(1,2,1),
             (3,1,3),
             (2,2,1),
             (1,1,2)]
    
    for (count, source, destination) in moves:
        stacks = update_stacks_with_crate_move(stacks, count, source, destination)


if __name__ == '__main__':
    try_example()
    solve()