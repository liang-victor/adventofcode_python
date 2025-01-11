def load_data():
    with open("input/day_7.txt") as f:
        data = f.read()
        return data

def process(data):
    data = data.split('\n')
    data = [d for d in data if d != '$ ls']

    directory_table = {}
    file_size_table = {}
    current_dir_contents = []
    current_path= ()

    for d in data:
        split = d.split(' ')
        if split[0] == '$' and split[1] == 'cd':
            if current_path and current_dir_contents:
                directory_table[current_path] = current_dir_contents.copy()
                current_dir_contents = []
            if split[2] == '..':
                current_path= current_path[:-1]
            else:
                current_path+= (split[2],)
        elif split[0] == 'dir':
            sub_directory = current_path + (split[1],)
            current_dir_contents.append(sub_directory)
        else:
            size = int(split[0])
            file_path = current_path + (split[1],)
            current_dir_contents.append(file_path)
            file_size_table[file_path] = size

    directory_table[current_path] = current_dir_contents
    return directory_table, file_size_table

def get_directory_size(name, directory_table, file_size_table):
    directory_size = 0
    for f in directory_table[name]:
        size = get_size(f, directory_table, file_size_table)
        directory_size += size
    return directory_size

def get_size(name, directory_table, file_size_table):
    size = file_size_table.get(name)
    if size:
        return size
    else:
        size = get_directory_size(name, directory_table, file_size_table)
        file_size_table[name] = size
        directory_size_table[name] = size
        return size

if __name__ == "__main__":
    data = load_data()
    directory_table, file_size_table = process(data)

    directory_size_table = {}
    root_size = get_size(('/',), directory_table, file_size_table)

    # part 1: sum of all directories smaller than 100000
    result = sum([d for d in directory_size_table.values() if d <= 100000])
    print(f'Part 1: {result}')

    # part 2: smallest directory that would free up 30000000
    total_disk_space = 70000000
    required_space = 30000000
    current_free_space = total_disk_space - root_size
    minimum_space_to_free = required_space - current_free_space

    result_2 = min([d for d in directory_size_table.values() if d >= minimum_space_to_free])
    print(f'Part 2: {result_2}')