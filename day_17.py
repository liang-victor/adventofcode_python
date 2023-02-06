ROCK_CHAR="@"
ROW_WIDTH=7
class Chamber:
    """

    self.rows[0] is the bottom of the chamber
    """

    def __init__(self):
        self.rows = ['·'*ROW_WIDTH for _ in range(4)]
        self.highest_rock = 0


    def visualize(self):
        for row in reversed(self.rows):
            print(f'|{row}|')
        print(f'+{"-"*ROW_WIDTH}+')

class Rock:
    def __init__(self):



def generate_rock(chamber):
    while True:
        chamber.highest_rock


if __name__=='__main__':
    chamber = Chamber()

    rock_generator = generate_rock(chamber)
    next(rock_generator)


    # spawn a rock, it will be spawned in open space
    # compute drop and wind
    # check if the rock has landed
    # add the rock to the chamber
    # update the highest rock position



    chamber.visualize()



    1100000
    1100000
    0000000

    1100000
    0011000
    1111000

    1100000
    0110000
