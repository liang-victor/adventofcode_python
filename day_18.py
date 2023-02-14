from collections import deque


def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read().split('\n')


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Cube{(self.x, self.y, self.z)}"

    def coords(self):
        return self.x, self.y, self.z

    def generate_adjacents_cubes(self):
        """generates face-adjacent cube coordinates"""
        yield (self.x - 1, self.y, self.z)
        yield (self.x + 1, self.y, self.z)
        yield (self.x, self.y + 1, self.z)
        yield (self.x, self.y - 1, self.z)
        yield (self.x, self.y, self.z + 1)
        yield (self.x, self.y, self.z - 1)

    def generate_neighbours(self):
        """generates all neighbours including diagonals and corners"""
        for delta_x in range(-2, 2):
            for delta_y in range(-2, 2):
                for delta_z in range(-2, 2):
                    if delta_x == 0 and delta_y == 0 and delta_z == 0:
                        continue
                    yield (self.x + delta_x, self.y + delta_y, self.z + delta_z)


if __name__ == '__main__':
    data = load_data('day_18')
    data = [d.split(',') for d in data]
    data = [[int(x) for x in d] for d in data]
    cubes = [Cube(x, y, z) for [x, y, z] in data]

    adjacent = {}
    for cube in cubes:
        for adj in cube.generate_adjacents_cubes():
            if adj in adjacent:
                adjacent[adj] = adjacent[adj] + 1
            else:
                adjacent[adj] = 1

    matches = 0
    for cube in cubes:
        matches += adjacent.get(cube.coords(), 0)

    surface_area = 6 * len(cubes) - matches
    print(f'Part 1: The total surface area is {surface_area}')

    """Part 2
    
    In part 1, we didn't care where the exposed surfaces were. In part 2, we care if it is part of the outside
    or enclosed. How do we determine this?
    
    Start with a set of adjacent cubes like we did in the first part.
    Pick one of the cubes. 
    Explore its neighbours
        - if it's a rock increment a counter for number of rock surfaces touching
        - if it's another adjacent cube, add it to a set of contiguous cubes
        - if it's neither, it's empty space and not of interest
        - explore unvisited contiguous cubes in the same manner
        - once the queue or stack is exhausted, pick another unvisited cube and figure out its contiguous neighbours
        - once all adjacent cubes have been visited, we should have a collection of sets of contiguous cubes
        - the one with the largest number of cubes should be the "outside" (unless there's some fancy geometry inside)
    
    
    """

    lava_cubes = set([cube.coords() for cube in cubes])
    neighbour_cubes = set()
    for cube in cubes:
        for neighbour in cube.generate_neighbours():
            if neighbour not in lava_cubes:
                neighbour_cubes.add(neighbour)

    max_surface_area = 0
    while neighbour_cubes:
        lava_faces = 0
        unvisited_cube = neighbour_cubes.pop()
        current_contiguous = set([unvisited_cube])
        print(f'we chose this cube randomly: {unvisited_cube}')
        queue = deque([unvisited_cube])
        while queue:
            (x, y, z) = queue.popleft()

            for neighbour in Cube(x, y, z).generate_adjacents_cubes():
                if neighbour in lava_cubes:
                    lava_faces += 1
                    print(f'found a lava face! count: {lava_faces}')
                elif neighbour in neighbour_cubes:
                    print(f'found a neighbour {neighbour}')
                    neighbour_cubes.remove(neighbour)
                    current_contiguous.add(neighbour)
                    queue.append(neighbour)

        print(f'These cubes are contiguous {current_contiguous}')
        max_surface_area = max(max_surface_area, lava_faces)

    print(f"Part 2: there are {max_surface_area} faces exposed")
