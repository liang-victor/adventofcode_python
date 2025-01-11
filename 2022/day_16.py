from collections import deque
from copy import deepcopy
from functools import cache
import time


def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read().split('\n')


class Valve:
    def __init__(self, name, flow_rate, neighbours):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbours = neighbours
        self.index = None

    def __repr__(self):
        return f'{self.name} {self.flow_rate}'

    def set_index(self, index):
        self.index = index


def parse(data):
    graph = {}
    for line in data:
        [valve, tunnels] = line.split(';')
        [valve_name, flow_rate] = valve.replace('Valve ', '').replace('has flow rate=', '').split(' ')
        tunnels = (tunnels.strip()
                   .replace('tunnels lead to valves ', '')
                   .replace('tunnel leads to valve ', '')
                   .split(', '))
        graph[valve_name] = Valve(valve_name, int(flow_rate), tunnels)
    return graph


def calculate_distances(graph):
    """Computes the distances from every key valve to every other key valve

    Many valves have a flow rate of zero - there is no value in stopping there, they are only passed on the way
    to key valves that can opened to contribute to our flow rate. This function calculates the distance of every key
    valve relative to each other.
    """

    distances = {}

    for valve in graph.values():
        # simplify the graph by ignoring the nodes with zero flow rate (except AA where we will start)
        if valve.name != "AA" and valve.flow_rate == 0:
            continue

        distances[valve.name] = {"AA": 0, valve.name: 0}

        visited = {valve.name}
        queue = deque([(0, valve)])

        while queue:
            distance, current_valve = queue.popleft()
            for neighbour_name in current_valve.neighbours:
                if neighbour_name in visited:
                    continue
                visited.add(neighbour_name)
                neighbour = graph[neighbour_name]
                updated_distance = distance + 1
                if neighbour.flow_rate:
                    distances[valve.name][neighbour_name] = updated_distance
                queue.append((updated_distance, neighbour))

        del distances[valve.name][valve.name]
        if valve.name != "AA":
            del distances[valve.name]["AA"]

    return distances


@cache
def dfs(time, valve, open_valves=0):
    """
    There is some combination of key valve visits that maximizes the pressure released.

    This DFS explores those combinations and keeps track of the maximum flow

    open_valves is a bitmask representation which key valves are open
    """
    maximum_flow = 0

    for neighour_name in distances[valve.name]:

        neighbour = graph[neighour_name]

        if valve_already_open(open_valves, neighbour):
            continue

        time_to_travel_to_node = distances[valve.name][neighour_name]
        valve_opening_time = 1
        remaining_time = time - time_to_travel_to_node - valve_opening_time
        if remaining_time <= 0:
            continue

        updated_open_valves = open_valve(open_valves, neighbour)

        maximum_flow = max(maximum_flow,
                           dfs(remaining_time, neighbour, updated_open_valves) + neighbour.flow_rate * remaining_time)

    return maximum_flow


def valve_already_open(open_valves, neighbour):
    return open_valves & bitmask(neighbour)


def bitmask(valve):
    """Creates a bitmask by left shifting (<<)

    e.g.
    index 1:   10
    index 2:  100
    index 3: 1000


    """
    return 1 << valve.index


def open_valve(open_valves, valve):
    """Bitwise OR to set the target valve value to 1"""
    return open_valves | bitmask(valve)


if __name__ == "__main__":
    data = load_data("day_16")
    graph = parse(data)

    distances = calculate_distances(graph)

    index = -1
    for valve in graph.values():
        if valve.name != 'AA' and valve.flow_rate > 0:
            index += 1
            valve.set_index(index)

    t_start = time.time()

    print(f'Part 1 result: {dfs(30, graph["AA"])}')

    print(f'Part 1 time: {time.time() - t_start} s')

    # part 2

    b = (1 << index + 1) - 1
    max_pressure_released = 0

    t_start = time.time()
    for valve_config in range(b // 2):
        inverse_valve_config = valve_config ^ b
        max_pressure_released = max(max_pressure_released,
                                    dfs(26, graph['AA'], valve_config) + dfs(26, graph['AA'], inverse_valve_config))

    print(f'Part 2 Max pressure released: {max_pressure_released}')
    print(f'part 2 time: {time.time() - t_start} s')
