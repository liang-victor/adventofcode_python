ROCK = '#'
SOURCE = '+'
SOURCE_LOCATION = 500
EMPTY = '·'
TRAIL = '~'
SAND = 'O'


def load(file):
    with open(f'input/{file}.txt') as f:
        lines = f.read().split('\n')

        coordinates = []
        for line in lines:
            coordinates.append([coord.split(',') for coord in line.split(' -> ')])
        return coordinates


def get_all_points(start, end):
    points = [start]
    (x_start, y_start) = start
    (x_end, y_end) = end
    (x_current, y_current) = start

    delta_x = x_end - x_start
    delta_y = y_end - y_start

    if delta_x > 0:
        for x in range(x_start, x_end, 1):
            (x_current, y_current) = (x + 1, y_current)
            points.append((x_current, y_current))
    elif delta_x < 0:
        for x in range(x_start, x_end, -1):
            (x_current, y_current) = (x - 1, y_current)
            points.append((x_current, y_current))
    elif delta_y > 0:
        for y in range(y_start, y_end, 1):
            (x_current, y_current) = (x_current, y + 1)
            points.append((x_current, y_current))
    elif delta_y < 0:
        for y in range(y_start, y_end, -1):
            (x_current, y_current) = (x_current, y - 1)
            points.append((x_current, y_current))
    return points


class Rock:
    def __init__(self, list_of_coordinates):
        self.vertices = []
        for [x, y] in list_of_coordinates:
            self.vertices.append((int(x), int(y)))

    def __repr__(self):
        return f"Rock: {self.vertices}"

    def coordinates(self):
        prev_vertex = self.vertices[0]
        all_coordinates = [prev_vertex]
        for curr_vertex in self.vertices[1:]:
            all_coordinates.extend([point for point in get_all_points(prev_vertex, curr_vertex)[1:]])
            prev_vertex = curr_vertex
        return all_coordinates

    def min_x(self):
        return min([v[0] for v in self.vertices])

    def max_x(self):
        return max([v[0] for v in self.vertices])

    def min_y(self):
        return min([v[1] for v in self.vertices])

    def max_y(self):
        return max([v[1] for v in self.vertices])


class Map:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.points = [[None for _x in range(min_x, max_x + 1)] for _y in range(min_y, max_y + 1)]

    def get_coord(self, coordinate):
        (x, y) = coordinate
        return self.points[y - self.min_y][x - self.min_x]

    def set_coord(self, coordinate, value):
        (x, y) = coordinate

        self.points[y - self.min_y][x - self.min_x] = value

    def visualize(self):
        # 3 line header
        for i in range(2, -1, -1):
            print(' ' * 4, end='')
            for x in range(self.min_x, self.max_x + 1):
                if x in [SOURCE_LOCATION, self.min_x, self.max_x]:
                    part_of_row_number = x % 10 ** (i + 1) // 10 ** i
                    print(part_of_row_number, end='')
                else:
                    print(' ', end='')
            print('\n', end='')

        # main grid with row number
        for y in range(self.min_y, self.max_y + 1):
            print(f'{y:3} ', end='')
            for x in range(self.min_x, self.max_x + 1):
                value = self.get_coord((x, y))
                if value:
                    print(value, end='')
                else:
                    print(EMPTY, end='')
            print('\n', end='')


class Grain:
    def __init__(self, map):
        self.x = SOURCE_LOCATION
        self.y = 0
        map.set_coord((self.x, self.y), SAND)

    def can_move(self, coordinate, map):
        return map.get_coord(coordinate) in [None, TRAIL]

    def move(self, destination, map):
        current_position = (self.x, self.y)
        map.set_coord(current_position, TRAIL)

        (self.x, self.y) = destination
        map.set_coord(destination, SAND)

    def drop(self, map):
        while True:
            if self.can_move(move_down := (self.x, self.y + 1), map):
                self.move(move_down, map)
            elif self.can_move(move_diagonal_left := (self.x - 1, self.y + 1), map):
                self.move(move_diagonal_left, map)
            elif self.can_move(move_diagonal_right := (self.x + 1, self.y + 1), map):
                self.move(move_diagonal_right, map)
            else:
                break


if __name__ == "__main__":
    data = load("day_14")
    # data = load("day_14_example")
    rocks = [Rock(coordinates) for coordinates in data]

    min_x = min([rock.min_x() for rock in rocks])
    max_x = max([rock.max_x() for rock in rocks])
    min_y = 0
    max_y = max([rock.max_y() for rock in rocks])

    map = Map(min_x, max_x, min_y, max_y)
    map.set_coord((SOURCE_LOCATION, 0), SOURCE)
    for rock in rocks:
        for coord in rock.coordinates():
            map.set_coord(coord, ROCK)

    for step in range(800):
        try:
            Grain(map).drop(map)
        except IndexError:
            print(f"the sand falls out of the map at step {step}")
            break

    map.visualize()

    # we need sufficient x-space to allow the pyramid of sand to build up
    # this requires max_y space on each side of the source
    max_y = max_y + 2
    min_x = SOURCE_LOCATION - max_y
    max_x = SOURCE_LOCATION + max_y

    map = Map(min_x, max_x, min_y, max_y)
    for rock in rocks:
        for coord in rock.coordinates():
            map.set_coord(coord, ROCK)
    for x in range(min_x, max_x + 1):
        map.set_coord((x, max_y), ROCK)

    for step in range(30000):
        Grain(map).drop(map)
        if map.get_coord((SOURCE_LOCATION, 0)) == SAND:
            print(f"the source of the sand is blocked at step: {step + 1}\n")
            break

    map.visualize()
