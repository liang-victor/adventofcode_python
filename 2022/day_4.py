"""--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
For the first few pairs, this list means:

Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
The Elves in the second pair were each assigned two sections.
The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.
This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

To begin, get your puzzle input.
"""

def load_data():
    with open("input/day_4.txt") as f:
        raw_data = f.read()
    return raw_data.split("\n")

class Range:
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)

    def __repr__(self):
        return f"Range: {self.start}-{self.end}"

    def contains(self, other):
        return other.start >= self.start and other.end <= self.end

    def in_range(self, value):
        return self.start <= value <= self.end

    def any_overlap(self, other):
        return self.in_range(other.start) or self.in_range(other.end) or self.contains(other) or other.contains(self) 

def process_ranges(data):
    paired_ranges = []
    for datum in data:
        [first_range, second_range] = datum.split(",")
        [first_start, first_end] = first_range.split("-")
        [second_start, second_end] = second_range.split("-")
        paired_ranges.append((Range(first_start, first_end), Range(second_start, second_end)))
    return paired_ranges

def solve():
    data = load_data()
    paired_ranges =  process_ranges(data)

    count_contains = 0
    for (first, second) in paired_ranges:
        if first.contains(second) or second.contains(first):
            count_contains += 1

    print(f"The number of pairs where one is wholly inside another is {count_contains}")
    
    count_overlap = 0
    for (first, second) in paired_ranges:
        if first.any_overlap(second):
            count_overlap += 1
    print(f'This many overlaps: {count_overlap}')

if __name__ == "__main__":
    solve()