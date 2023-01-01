"""--- Day 3: Rucksack Reorganization ---

One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
The fourth rucksack's compartments only share item type v.
The fifth rucksack's compartments only share item type t.
The sixth rucksack's compartments only share item type s.
To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
"""

def load_data():
    with open("input/day_3.txt") as f:
        raw_data = f.read()
    return raw_data.split("\n")

def group_intersections(group):
    group_sets = [set(rucksack) for rucksack in group] 
    accum_intersection = group_sets[0]
    for elf in group_sets[1:]:
        accum_intersection = accum_intersection.intersection(elf)
    return accum_intersection

def solve():
    rucksacks = load_data()

    split_rucksacks = []
    for rucksack in rucksacks:
        midpoint = int(len(rucksack)/2)
        split_rucksacks.append((rucksack[:midpoint], rucksack[midpoint:]))
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_score = {alpha:i+1 for i, alpha in enumerate(alphabet)}


    score = 0
    for first_compartment, second_compartment in split_rucksacks:
        common_items = set(first_compartment).intersection(set(second_compartment))
        
        for char in common_items:
            if char.islower():
                score += alphabet_score[char]
            else:
                score += alphabet_score[char.lower()] + 26

    print(f'Score part 1: {score}')

    group_size = 3
    groups = []
    current_group = []

    for i, rucksack in enumerate(rucksacks):
        current_group.append(rucksack)
        if (i+1)%3==0:
            groups.append(current_group)
            current_group = []

    intersections = [group_intersections(group) for group in groups]
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_score = {alpha:i+1 for i, alpha in enumerate(alphabet)}

    group_score = 0
    for group in intersections:
        for char in group:
            if char.islower():
                group_score += alphabet_score[char]
            else:
                group_score += alphabet_score[char.lower()] + 26
    print(f'Score part 1: {group_score}')

"""Part Two ---
As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?"""

if __name__ == '__main__':
    solve()