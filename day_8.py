def load_data():
    with open("input/day_8.txt") as f:
        data = f.read()
        return data

def process_rows(data):
    processed = []
    for row in data.split('\n'):
        processed.append([int(char) for char in row])
    return processed

def check_viewable_from_left(viewable, rows):
    for j, row in enumerate(rows):
        current_height = -1
        for i, value in enumerate(row):
            if value > current_height:
                # print(f'{value} at ({i}, {j})')
                viewable.add((i,j))
                current_height = value
    return viewable

def check_viewable_from_right(viewable, rows):
    for j, row in enumerate(rows):
        current_height = -1
        for i in range(horizontal_trees-1, 0, -1):
            value = row[i]
            # print(f'{value} at ({i}, {j})')
            if value > current_height:
                viewable.add((i,j))
                current_height = value
    return viewable

def check_viewable_from_above(viewable, rows):
    for i in range(horizontal_trees):
        current_height = -1
        for j in range(vertical_trees):
            value = rows[j][i]
            # print(f'{value} at ({i}, {j})')
            if value > current_height:
                viewable.add((i,j))
                current_height = value
    return viewable

def check_viewable_from_below(viewable, rows):
    for i in range(horizontal_trees):
        current_height = -1
        for j in range(vertical_trees-1, 0, -1):
            value = rows[j][i]
            if value > current_height:
                viewable.add((i,j))
                current_height = value
    return viewable

def visualize_viewable(viewable):
    for j in range(vertical_trees):
        for i in range(horizontal_trees):
            if (i,j) in viewable:
                print('X', end='')
            else:
                print('-', end='')
        print('')

def count_trees_viewable(position, rows):
    # get value at tree
    (i,j) = position
    tree_value = rows[j][i]
    
    # scan from value i-1 to 0 and count
    view_left = 0
    for ix in range(i-1, -1, -1):
        current_tree = rows[j][ix]
        if current_tree >= tree_value:
            view_left +=1
            break
        else:
            view_left +=1


    # scan from value i+1 to horizontal_trees and count
    view_right = 0 
    for ix in range(i+1, horizontal_trees):
        current_tree = rows[j][ix]
        if current_tree >= tree_value:
            view_right +=1
            break
        else:
            view_right +=1

    # scan from value j-1 to 0
    view_up = 0
    for jx in range(j-1, -1, -1):
        current_tree = rows[jx][i]
        if current_tree >= tree_value:
            view_up += 1
            break
        else:
            view_up += 1
        
    # scan from value j+1 to vertical_trees-1
    view_down = 0
    for jx in range(j+1, vertical_trees):
        current_tree = rows[jx][i]
        if current_tree >= tree_value:
            view_down += 1
            break
        else:
            view_down += 1

    return view_left * view_right * view_up * view_down

if __name__ == '__main__':
    data = load_data()

    rows = process_rows(data)

    viewable = set()
    horizontal_trees = len(rows[0])
    vertical_trees = len(rows)

    viewable = check_viewable_from_left(viewable, rows)
    viewable = check_viewable_from_right(viewable, rows)
    viewable = check_viewable_from_above(viewable, rows)
    viewable = check_viewable_from_below(viewable, rows)

    # visualize_viewable(viewable)
    print(f'total viewable trees: {len(viewable)}')

    max_view = 0 
    for tree in viewable:
        view = count_trees_viewable(tree, rows)
        if view > max_view:
            max_view = view


    print(f'max view: {max_view}')