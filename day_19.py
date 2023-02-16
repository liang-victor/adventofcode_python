"""

Every robot costs ore, some cost an additional resource
Our final product is cracked geodes - so if you can afford a geode robot - buy it!
There is a progression from clay -> obsidian -> geode


"""
import re


class Blueprint:
    def __init__(self, id, ore_robot_cost, clay_robot_cost, obsidian_ore_cost,
                 obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        self.id = id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_ore_cost = obsidian_ore_cost
        self.obsidian_clay_cost = obsidian_clay_cost
        self.geode_ore_cost = geode_ore_cost
        self.geode_obsidian_cost = geode_obsidian_cost

    def __repr__(self):
        return f'Blueprint {self.id}'

    def simulate(self, max_time):
        state = MiningState()
        time = 0

        while time <= max_time:
            print(f'Time: {time}')
            if state.ore >= self.geode_ore_cost and state.obsidian >= self.geode_obsidian_cost:
                print("buy a geode robot!")
                state.ore -= self.geode_ore_cost
                state.obsidian -= self.geode_obsidian_cost
                state.geode_robots += 1

            if state.ore >= self.obsidian_ore_cost and state.clay >= self.obsidian_clay_cost:
                print("buy an obsidian robot!")
                state.ore -= self.obsidian_ore_cost
                state.clay -= self.obsidian_clay_cost
                state.clay_robots += 1

            if state.ore >= self.clay_robot_cost:
                print("buy a clay robot!")
                state.ore -= self.clay_robot_cost
                state.clay_robots += 1
            state.update_mining()
            print(state)
            time += 1
            print()


class MiningState:
    def __init__(self, ore_robots=1, clay_robots=0, obsidian_robots=0, geode_robots=0):
        self.ore_robots = ore_robots
        self.clay_robots = clay_robots
        self.obsidian_robots = obsidian_robots
        self.geode_robots = geode_robots
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

    def __repr__(self):
        return f"State: ore: {self.ore}, clay: {self.clay}, obsidian: {self.obsidian}, geode: {self.geode}"

    def update_mining(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geode += self.obsidian_robots


def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read().split('\n')


def process_data(data):
    blueprints = []
    for d in data:
        numbers = re.findall(r'\d+', d)
        numbers = [int(x) for x in numbers]
        blueprints.append(Blueprint(*numbers))
    return blueprints


if __name__ == "__main__":
    data = load_data("day_19_example")
    blueprints = process_data(data)
    print(blueprints)
    blueprints[0].simulate(24)
