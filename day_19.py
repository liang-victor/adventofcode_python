"""

Every robot costs ore, some cost an additional resource
Our final product is cracked geodes - so if you can afford a geode robot - buy it!
There is a progression from clay -> obsidian -> geode


"""
import re


MAX_TIME = 25

class MiningState:
    def __init__(self,
                 ore_robots=1,
                 clay_robots=0,
                 obsidian_robots=0,
                 geode_robots=0,
                 ore=0,
                 clay=0,
                 obsidian=0,
                 geode=0,
                 time=0):
        self.robots = {"ore": ore_robots,
                       "clay": clay_robots,
                       "obsidian": obsidian_robots,
                       "geode": geode_robots}
        self.resources= {"ore": ore,
                       "clay": clay,
                       "obsidian": obsidian,
                       "geode": geode}
        # self.ore_robots = ore_robots
        # self.clay_robots = clay_robots
        # self.obsidian_robots = obsidian_robots
        # self.geode_robots = geode_robots
        # self.ore = ore
        # self.clay = clay
        # self.obsidian = obsidian
        # self.geode = geode
        self.time = time

    def __repr__(self):
        return f"State: ore: {self.ore}, clay: {self.clay}, obsidian: {self.obsidian}, geode: {self.geode}"

    def update_mining(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geode += self.obsidian_robots

    def is_generating(self, resource):
        # todo: use case here? enum too?
        if resource == "ore":
            return self.ore_robots > 0
        if resource == "clay":
            return self.clay_robots > 0
        if resource == "obsidian":
            return self.obsidian_robots > 0
        if resource == "geode":
            return self.geode_robots > 0
        raise f"Unknown resource {resource}"

    def time_to_buy_next_robot(self, robot_type, blueprint):
        if robot_type == "ore":
            resource_required = blueprint.ore_robot_cost - self.ore
            if resource_required % self.ore_robots ==0:
                return resource_required // self.ore_robots
            else:
                return resource_required // self.ore_robots + 1

        elif robot_type == "clay":
            resource_required =  blueprint.clay_robot_cost - self.clay
            if resource_required % self.ore_robots == 0:
                return resource_required // self.ore_robots
            else:
                return resource_required // self.ore_robots + 1
class Blueprint:
    def __init__(self, id, ore_robot_cost, clay_robot_cost, obsidian_ore_cost,
                 obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        self.id = id
        self.ore_robot_cost = self.cost_map(ore=ore_robot_cost)
        self.clay_robot_cost = self.cost_map(ore=clay_robot_cost)
        self.obsidian_robot_cost = self.cost_map(ore=obsidian_ore_cost,
                                               clay=obsidian_clay_cost)
        self.geode_robot_cost = self.cost_map(ore=geode_ore_cost,
                                            obsidian=geode_obsidian_cost)
    @staticmethod
    def cost_map(self, ore=0, clay=0, obsidian=0):
        return {"ore": ore, "clay": clay, "obsidian": obsidian}

    def __repr__(self):
        return f'Blueprint {self.id}'
    def simulate(self, max_time):
        state = MiningState()
        time = 0

        """
        from a given state, we have have a few options:
            - accumulate the ore to buy another ore robot
            - accumulate the ore to buy another clay robot
            if I have at least one clay robot:
                - accumulate the ore and clay to buy an obsidian robot
            if I have at least one obsidian robot:
                - accumulate the ore and obsidian to buy a geode robot
            - I can also accumulate resources to the time limit    
            
            ^ for each above option there is time cost to accumulate the resource necessary
            (should that be part of the state? or packaged alongside the state?)
            compute the resulting state and time for each choice
             - put those states in the stack and simulate from those states 
             - alternatively call simulate recursively on those states and keep the one with the highest geode count at the time limit
            
            
        """

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

    def dfs_max_geodes(self, state: MiningState):
        if state.is_generating("ore") and time_cost :=


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
