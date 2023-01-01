def load_data():
    with open("input/day_6.txt") as f:
        raw_data = f.read()
    return raw_data

def find_window_of_unique_characters(data, window_size):
      for i in range(len(data)):
        latest = i + window_size
        latest_window = data[i:latest]
        if len(set(latest_window)) == window_size:
            return latest


def solve():
    data = load_data()

    # part 1: looking for window of size 4 with 4 unique characters
    packet_marker = find_window_of_unique_characters(data, 4)
    print(f"Packet Marker: {packet_marker}")
    
    # part 2: window of size 14 
    message_marker = find_window_of_unique_characters(data, 14)
    print(f"Message Marker: {message_marker}")

if __name__ == '__main__':
    solve()