ROCK_CHAR = "@"
CHAMBER_WIDTH = 7


def binary(n):
    return f'{n:07b}'


class Chamber:
    """

    self.rows[0] is the bottom of the chamber

    Row contents are stored as binary numbers
    e.g. 0001110 means there is a rock in columns 3, 4 and 5

    We can do bitwise AND to check for collisions
    """

    def __init__(self):
        self.rows = [0 for _ in range(4)]
        self.highest_rock = 0

    def visualize(self, rock=None):
        for i, row in enumerate(reversed(self.rows)):
            row_number = len(self.rows) - 1 - i
            row_string = f"{row:07b}".replace('0', '·').replace('1', '#')
            if rock and row_number in rock.rows.keys():
                index = rock.rows.get(row_number)
                # TODO: render rocks that span multiple rows (do this check differently? store value in rock.rows differently?)
                row_string = rock.draw_on(row_string, index)

            print(f'|{row_string}|  {row_number}')
        print(f'+{"=" * CHAMBER_WIDTH}+')

    def get_row(self, height):
        return self.rows[height]

    def absorb_rock(self, rock):
        for chamber_row_number, index in rock.rows.items():
            existing_chamber_row = self.rows[chamber_row_number]
            self.rows[chamber_row_number] = existing_chamber_row | rock.generate_bitmask(index)

        # update the highest point of rock
        self.highest_rock = max(self.highest_rock, max(rock.rows.keys()))

        # add more rows above the high point if necessary
        if (rows_needed := self.highest_rock + 4 - len(self.rows)) > 0:
            self.rows.extend([0] * rows_needed)


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

    def __repr__(self):
        return f"rock at {self.height} {self.column}"

    def generate_bitmask(self, index=0):

        # this is going to be different depending on the shape, and which row we're calculating for
        return self.shape[index] << CHAMBER_WIDTH - self.max_width - self.column

    def update_rows(self):
        self.rows = {(self.height + x): x for x in range(len(self.shape))}

    def draw_on(self, string, index=0):
        """Replaces characters in the string if the rock occupies those spaces"""
        # for i, (r, c) in enumerate(zip(self.generate_string(), string)):
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
        # bitwise & to check potential collision
        # print(binary(chamber.get_row(self.height - 1)))

        # print(binary(self.generate_bitmask()))
        will_collide_below = chamber.get_row(self.height - 1) & self.generate_bitmask()
        above_ground = self.height > 0
        return above_ground and not will_collide_below


class HorizontalStick(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("1111", 2)]
        self.max_width = 4


class Plus(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("10", 2), int("111", 2), int("10", 2)]
        self.max_width = 3


class ReverseL(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("111", 2), int("1", 2), int("1", 2)]
        self.max_width = 3


class VerticalStick(Rock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape = [int("1", 2)] * 4
        self.max_width = 1


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


def rock_factory(rock_cycler, start_height, start_column=2):
    rock = next(rock_cycler)
    rock.height = start_height
    rock.column = start_column
    rock.update_rows()

    return rock


if __name__ == '__main__':
    chamber = Chamber()
    # chamber.rows[0] = int("0100001", 2)
    rock_cycler = rock_cycle()

    for round in range(8):
        rock = rock_factory(rock_cycler, chamber.highest_rock + 3)
        while rock.falling:
            rock.drop()
            if not rock.can_drop(chamber):
                rock.falling = False

            # simulate rock pushed by wind

            # # check the next iteration before looping around
            # if not rock.can_drop(chamber):
            #     rock.falling = False
        chamber.absorb_rock(rock)
        # chamber.visualize(None)

        chamber.visualize(rock)
        print()

    # merge rock into chamber

    # current_rock.drop()
    # print(current_rock)
    # print(f'|{current_rock[0]:07b}|')
    # spawn a rock, it will be spawned in open space
    # compute drop and wind
    # check if the rock has landed
    # add the rock to the chamber
