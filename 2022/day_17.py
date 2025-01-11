ROCK_CHAR = "@"
CHAMBER_WIDTH = 7


def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read()


def binary(n):
    return f'{n:07b}'


class Chamber:
    """

    self.rows[0] is the bottom of the chamber

    Highest rock position is the number that can still be filled
    e.g. if there is a rock at height 2, highest rock position is now 3

    Row contents are stored as binary numbers
    e.g. 0001110 means there is a rock in columns 3, 4 and 5

    We can do bitwise AND to check for collisions
    """

    def __init__(self):
        self.rows = [0 for _ in range(4)]
        self.highest_rock = 0

    def __getitem__(self, row_index):
        rows_to_add = row_index - len(self.rows) + 1
        if rows_to_add > 0:
            self.rows.extend([0] * rows_to_add)
            return 0
        else:
            return self.rows[row_index]

    def __setitem__(self, row_index, value):
        self.rows[row_index] = value

    def visualize(self, rock=None, limit=30):
        for i, row in enumerate(reversed(self.rows)):
            if limit and i > limit:
                break
            row_number = len(self.rows) - 1 - i
            row_string = f"{row:07b}".replace('0', '·').replace('1', '#')
            if rock and row_number in rock.rows.keys():
                index = rock.rows.get(row_number)
                row_string = rock.draw_on(row_string, index)

            print(f'|{row_string}|  {row_number}')
        print(f'+{"=" * CHAMBER_WIDTH}+')

    def get_row(self, height):
        return self.rows[height]

    def absorb_rock(self, rock):
        for chamber_row_number, index in rock.rows.items():
            existing_chamber_row = self[chamber_row_number]
            self[chamber_row_number] = existing_chamber_row | rock.generate_bitmask(index)

        self.highest_rock = max(self.highest_rock, max(rock.rows.keys()) + 1)

    def top_n_rows(self, n):
        """Returns n rows starting from the highest rock"""
        return tuple(self.rows[self.highest_rock:self.highest_rock - n:-1])


class Rock:
    """
    A rock's position (column, height) is the location of the bottom left corner of the rock
    Note that in the case of the + shaped rock, this position corresponds to a spot not occupied by rock

    Shape contains a list of values, from bottom to up
    e.g.
        010           1 << 1 = 2
        111           7
        000           2

    To materialize the rock's shape into a row, we need to bit shift the shape by its width and column position

    """

    def __init__(self):
        self.height = None
        self.column = None
        self.falling = True
        self.max_width = None
        self.shape = None
        self.rows = None
        self.type = None

    def __repr__(self):
        return f"rock at {self.height} {self.column}"

    def generate_bitmask(self, index=0, right_shift=0, left_shift=0):
        return self.shape[index] << CHAMBER_WIDTH - self.max_width - self.column >> right_shift << left_shift

    def update_rows(self):
        self.rows = {(self.height + x): x for x in range(len(self.shape))}

    def draw_on(self, string, index=0):
        """Replaces characters in the string if the rock occupies those spaces"""

        chars = []
        bitmask_string = binary(self.generate_bitmask(index))
        for char, bit_char in zip(string, bitmask_string):
            if bit_char == "1":
                chars.append(ROCK_CHAR)
            else:
                chars.append(char)
        return ''.join(chars)

    def drop(self):
        self.height -= 1
        self.update_rows()

    def can_drop(self, chamber):
        will_collide_below = 0
        for chamber_row, index in self.rows.items():
            current_row_will_collide = chamber[max(chamber_row - 1, 0)] & self.generate_bitmask(index=index)
            will_collide_below = will_collide_below | current_row_will_collide
        above_ground = self.height > 0
        return above_ground and not will_collide_below

    def move_right(self):
        self.column += 1

    def move_left(self):
        self.column -= 1

    def can_move_right(self, chamber):
        can_move = True
        for row_number, index in self.rows.items():
            right_edge_at_wall = 1 & self.generate_bitmask(index)
            chamber_collision = chamber[row_number] & self.generate_bitmask(index, right_shift=1)
            can_move = can_move and not right_edge_at_wall and not chamber_collision
        return can_move

    def can_move_left(self, chamber):
        can_move = True
        for row_number, index in self.rows.items():
            left_edge_at_wall = (1 << (CHAMBER_WIDTH - 1)) & self.generate_bitmask(index)
            chamber_collision = chamber[row_number] & self.generate_bitmask(index, left_shift=1)
            can_move = can_move and not left_edge_at_wall and not chamber_collision
        return can_move

    def push_by_wind(self, direction, chamber):
        match direction:
            case ">":
                if self.can_move_right(chamber):
                    self.move_right()

            case "<":
                if self.can_move_left(chamber):
                    self.move_left()


class HorizontalStick(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("1111", 2)]
        self.max_width = 4
        self.type = "horizontal_stick"


class Plus(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("10", 2), int("111", 2), int("10", 2)]
        self.max_width = 3
        self.type = "plus"


class ReverseL(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("111", 2), int("1", 2), int("1", 2)]
        self.max_width = 3
        self.type = "reverse_l"


class VerticalStick(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("1", 2)] * 4
        self.max_width = 1
        self.type = "vertical_stick"


class Box(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("11", 2)] * 2
        self.max_width = 2


def rock_cycle():
    while True:
        yield HorizontalStick()
        yield Plus()
        yield ReverseL()
        yield VerticalStick()
        yield Box()


def rock_factory(rock_cycler, start_height, start_column=2) -> Rock:
    rock = next(rock_cycler)
    rock.height = start_height
    rock.column = start_column
    rock.update_rows()

    return rock


def wind_cycle(input):
    while True:
        for direction in input:
            yield direction


if __name__ == '__main__':
    input = load_data('day_17')
    wind_generator = wind_cycle(input)

    chamber = Chamber()
    rock_cycler = rock_cycle()

    for round in range(0, 2022):
        rock = rock_factory(rock_cycler, chamber.highest_rock + 4)
        while True:
            if rock.can_drop(chamber):
                rock.drop()
            else:
                chamber.absorb_rock(rock)
                break

            rock.push_by_wind(next(wind_generator), chamber)
    chamber.visualize(limit=20)
    print(f'Part 1 highest rock: {chamber.highest_rock}')

    # Part 2: Let's see if we can find a cycle

    wind_generator = wind_cycle(input)
    chamber = Chamber()
    rock_cycler = rock_cycle()
    seen_states = {}
    target_rounds = 1_000_000_000_000
    running_total = 0
    save_states = True
    remaining_rounds = None

    for round in range(0, 5000):
        rock = rock_factory(rock_cycler, chamber.highest_rock + 4)
        wind_direction = next(wind_generator)
        while True:

            if rock.can_drop(chamber):
                rock.drop()
            else:
                chamber.absorb_rock(rock)
                break

            if not wind_direction:
                wind_direction = next(wind_generator)
            rock.push_by_wind(wind_direction, chamber)
            wind_direction = None

        chamber_state = chamber.top_n_rows(20)
        state = (rock.type, chamber_state, wind_direction)

        if save_states and state in seen_states:
            previous_round, previous_height = seen_states[state]
            current_round = round
            current_height = chamber.highest_rock

            number_of_cycles = (target_rounds - previous_round) // (current_round - previous_round)
            remaining_rounds = (target_rounds - previous_round) % (current_round - previous_round)
            height_per_cycle = current_height - previous_height

            print(
                f"result is {previous_height} + {number_of_cycles}*{height_per_cycle} + simulate {remaining_rounds} more rounds")
            running_total += previous_height + number_of_cycles * height_per_cycle

            save_states = False
            previous_height = current_height

        elif save_states:
            seen_states[state] = round, chamber.highest_rock

        if remaining_rounds and remaining_rounds >= 0:
            current_height = chamber.highest_rock
            running_total += (current_height - previous_height)
            previous_height = current_height

            if remaining_rounds == 0:
                break

            remaining_rounds -= 1

    print(f"after 1 trillion rounds, the height is {running_total}")
