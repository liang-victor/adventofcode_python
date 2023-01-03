INFINITY = 999

def load_data():
    with open("input/day_12.txt") as f:
        return f.read().split('\n')

def value_at(coordinate):
    """
    Axes
    ----> x
    |
    |
    v y
    """

    (x, y) = coordinate
    value = data[y][x]
    if value == 'S':
        value = 'a'
    elif value == 'E':
        value = 'z'
    return value

def height_at(coordinate):
    return ord(value_at(coordinate))

def find_coordinates(data, target_value):
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == target_value:
                return (x,y)

def check_valid_moves(current_location, ascending=True):
    (x,y) = current_location
    up = (x, y+1)
    down = (x, y-1)
    left = (x-1, y)
    right = (x+1, y)

    valid_moves = []
    for destination in [up, down, left, right]:
        if within_board(destination):
            if ascending and height_at(destination) - height_at(current_location)<=1:
                valid_moves.append(destination)
            elif not ascending and height_at(current_location) - height_at(destination) <=1:
                valid_moves.append(destination)
    return valid_moves

def within_board(coordinate):
    (x,y) = coordinate

    max_x = len(data[0])
    max_y = len(data)
    return (0 <= x < max_x) and (0 <= y < max_y)

def closeness_to_destination(coordinate):
    (x,y) = coordinate
    return hill_map[y][x].closeness_to_destination

def node_at(coordinate):
    (x,y) = coordinate
    return hill_map[y][x]

def reset_map(data):
    hill_map = []
    for y, row in enumerate(data):
        map_row = [Node((x,y), target) for x, _ in enumerate(row)]
        hill_map.append(map_row)
    return hill_map

class Node:
    def __init__(self, coordinate, target):
        (x,y) = coordinate
        self.x = x
        self.y = y
        self.value = value_at(coordinate)
        self.height = height_at(coordinate) - ord('a')
        self.moves = INFINITY
        self.coming_from = None
        self.closeness_to_destination = self.calculate_closeness_to_destination(target)
        

    def __repr__(self):
        return f"{self.height}"

    def calculate_closeness_to_destination(self, target):
        """
        Taking taxicab distance as the measure of closeness
        Use this to prioritize which routes to investigate
        """
        (x_t, y_t) = target
        target_height = height_at(target) - ord('a')

        delta_x = x_t - self.x
        delta_y = y_t - self.y
        delta_h = target_height - self.height
 
        return abs(delta_x) + abs(delta_y) + abs(delta_h)
    
    def set_moves(self, value, coming_from):
        self.moves = value
        self.coming_from = coming_from

def visualize_height(hill_map):
    print("Height")
    for row in hill_map:
        for node in row:
            print(f'{node.height:3}', end='')
        print('\n', end='')
    print("")

def visualize_moves(hill_map):
    print("Minimum moves from the start (so far)")
    for row in hill_map:
        for node in row:
            print(f'{node.moves:3}', end='')
        print('\n', end='')
    print('')

def visualize_closeness_to_destination(hill_map):
    print("Closeness to destination (smaller is closer)")
    for row in hill_map:
        for node in row:
            print(f'{node.closeness_to_destination: 3}', end='')
        print('\n', end='')
    print('')

def visualize_path(hill_map, start, target):
    current_node = target
    path_map = {}
    while current_node != start:
        prev = node_at(current_node).coming_from
        if prev:
            (p_x, p_y) = prev
            if node_at(current_node).x - p_x == 1:
                path_map[current_node] = '>'
            elif node_at(current_node).x - p_x == -1:
                path_map[current_node] = '<'
            elif node_at(current_node).y - p_y == 1:
                path_map[current_node] ='V'
            elif node_at(current_node).y - p_y == -1:
                path_map[current_node] ='^'
        current_node = prev


    print("Visualization of path:")
    for y, row in enumerate(hill_map):
        for x, _ in enumerate(row):
            s = path_map.get((x,y), '-')
            print(s, end='')
        print('\n', end='')
    print('')        


def find_fewest_steps_to_target(start, target, ascending=True):
    nodes_to_check = [start]
    visited = []
    node_at(start).set_moves(0, None)
    current_node = start
    moves = 0
    
    while node_at(target).moves == INFINITY: 
        moves += 1
        destination_nodes = []
        for current_node in nodes_to_check:
            if current_node not in visited:
                visited.append(current_node)
                valid_moves = sorted(check_valid_moves(current_node, ascending), key=closeness_to_destination)
                for coord in valid_moves:
                    if moves < node_at(coord).moves:
                        node_at(coord).set_moves(moves, current_node)
                destination_nodes.extend(valid_moves)
        nodes_to_check = destination_nodes

    return node_at(target).moves

def find_fewest_steps_to_target_height(start, target_height, ascending=True):
    nodes_to_check = [start]
    visited = []
    node_at(start).set_moves(0, None)
    current_node = start
    moves = 0

    while True:
        moves += 1
        destination_nodes = []
        for current_node in nodes_to_check:
            if current_node not in visited:
                visited.append(current_node)
                valid_moves = sorted(check_valid_moves(current_node, ascending), key=closeness_to_destination)
                for coord in valid_moves:
                    if moves < node_at(coord).moves:
                        node_at(coord).set_moves(moves, current_node)
                    if node_at(coord).height == target_height:
                        return node_at(coord).moves
                destination_nodes.extend(valid_moves)
        nodes_to_check = destination_nodes
    
if __name__ == '__main__':
    data = load_data()

    start = find_coordinates(data, 'S')
    target = find_coordinates(data, 'E')

    hill_map = reset_map(data)
    steps_to_target = find_fewest_steps_to_target(start, target)
    visualize_path(hill_map, start, target)
    
    print(f'This many moves to reach the target from {start}: {steps_to_target}')

    """Part 2: see if another starting point of height a is available

    there are many possible starting points, checking them all would be computationally intensive!
    meanwhile the path is more constrained around the summit, let's flip it around and find the first 
    point it meets at height a
    """

    start = find_coordinates(data, 'E')
    target_height = 0

    hill_map = reset_map(data)
    steps_to_target = find_fewest_steps_to_target_height(start, target_height, ascending=False)
   
    print(f'This many moves to reach height {target_height} target from {start}: {steps_to_target}')