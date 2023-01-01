def load_data():
    with open("input/day_9.txt") as f:
        data = f.read()
        return data

def process(data):
    moves = data.split('\n')
    moves = [move.split(' ') for move in moves]
    moves = [(move[0], int(move[1])) for move in moves]
    return moves

def split_move(move):
    """Splits longer moves into unit moves"""
    (direction, distance) = move
    for _ in range(distance):
        yield (direction, 1)  

def visualize(head, tail):
    max_x = 5
    max_y = 4

    for y in range(max_y, -1, -1):
        for x in range(max_x+1):
            if (x, y) == head:
                print('H', end='')
            elif (x, y) == tail:
                print('T', end='')
            elif (x, y) == (0,0):
                print('s', end='')
            else:
                print('-', end='')
        print('\n', end='')

def visualize_rope(rope, min_x = 0, max_x = 5, min_y = 0, max_y = 4):
    marked_positions = {}
    for i, position in enumerate(rope):
        if position not in marked_positions:
            if i == 0:
                marker = 'H'
            else:
                marker = i
            marked_positions[position] = marker
    if (0,0) not in marked_positions:
        marked_positions[(0,0)] = 's'

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x+1):
            if (x,y) in marked_positions:
                print(marked_positions[(x,y)], end='')
            else:
                print('-', end='')
        print('\n', end='')
    print('\n')

def apply_unit_move(move, head, tail):
    head = move_head(move, head)
    tail = follow(head, tail)
    return head, tail

def move_rope(move, rope):
    new_rope_position = []
    for i, knot in enumerate(rope):
        if i==0:
            position = move_head(move, knot)
        else:
            position = follow(position, knot)
        new_rope_position.append(position)
    return new_rope_position

def move_head(move, head):
    (direction, distance) = move
    (x, y) = head
    if direction == 'U':
        return (x, y + distance)
    if direction == 'D':
        return (x, y - distance)
    if direction == 'L':
        return (x-distance, y)
    if direction == 'R':
        return (x+distance, y)

def follow(head, tail):
    (x_head, y_head) = head 
    (x_tail, y_tail) = tail

    delta_x = x_head - x_tail
    delta_y = y_head - y_tail

    # not enough movement for tail to move
    if abs(delta_x) <= 1 and abs(delta_y) <= 1:
        return (x_tail, y_tail)

    # horizontal only
    if abs(delta_x) == 2 and delta_y == 0:
        return (x_tail + int(delta_x/2), y_tail)
    
    # vertical only
    if abs(delta_y) == 2 and delta_x == 0:
        return (x_tail, y_tail + int(delta_y/2))

    # diagonals
    if abs(delta_x) == 2 and abs(delta_y) == 1:
        return (x_tail + int(delta_x/2), y_tail + delta_y)

    if abs(delta_y) == 2 and abs(delta_x) == 1:
        return (x_tail + delta_x, y_tail + int(delta_y/2))

    if abs(delta_x) == 2 and abs(delta_y) == 2:
        return(x_tail + int(delta_x/2), y_tail + int(delta_y/2))
    
if __name__ == '__main__':
    data = load_data()
    moves = process(data)

    head = (0,0)
    tail = (0,0)
    visited = set([tail])

    for move in moves:
        # print(f'== {move[0]} {move[1]} ==\n')
        for unit_move in split_move(move):
            head, tail = apply_unit_move(unit_move, head, tail)
            visited.add(tail)
            # visualize(head, tail)

    print(f"Part 1: tail has visited {len(visited)} positions")

    # part 2: use a long rope 
    rope = [(0,0) for p in range(10)]
    visited_part_2 = set([(0,0)])
    for move in moves:
        print(f'== {move[0]} {move[1]} ==')
        for unit_move in split_move(move):
            rope = move_rope(unit_move, rope)

            tail = rope[-1]
            visited_part_2.add(tail)
        # visualize_rope(rope, -11, 14, -5, 16)

    print(f"Part 2: long tail has visited {len(visited_part_2)} positions")