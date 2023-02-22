"""

Every robot costs ore, some cost an additional resource
Our final product is cracked geodes - so if you can afford a geode robot - buy it!
There is a progression from clay -> obsidian -> geode


"""
import re
from copy import deepcopy

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

    def simulate_turns(self, turns):
        updated_state = deepcopy(self)
        """Returns a new state with incremented values"""
        for _turn in range(turns):
            for resource in ['ore', 'clay', 'obsidian', 'geode']:
                updated_state.resources[resource] += updated_state.robots[resource]
            updated_state.time += 1

        return updated_state


    def is_generating(self, resource):
        return self.robots.get(resource) > 0

    def time_to_buy_next_robot(self, robot_type, blueprint):
        # for each robot type, fetch the cost map
        # check the number of turns needed to reach that value
        # the maximum number determines number of turns needed
        # using that maximum number, determine amount of all resources generated

        cost_map = blueprint.get_costs(robot_type)
        turns = self.turns_to_build(cost_map)





        # if resource == "ore":
        #     resource_required = blueprint.ore_robot_cost[resource] - self.resources
        #     if resource_required % self.ore_robots ==0:
        #         return resource_required // self.ore_robots
        #     else:
        #         return resource_required // self.ore_robots + 1
        #
        # elif robot_type == "clay":
        #     resource_required =  blueprint.clay_robot_cost - self.clay
        #     if resource_required % self.ore_robots == 0:
        #         return resource_required // self.ore_robots
        #     else:
        #         return resource_required // self.ore_robots + 1

    def turns_to_build(self, cost_map):
        """Returns the number of turns needed to build the robot, based on the bottlenecking resource"""
        turns = 0
        for resource, cost in cost_map.items():
            required = cost - self.resources[resource]
            if required % self.robots[resource] == 0:
                turns = max(turns, required // self.robots[resource])
            else:
                turns = max(turns, required // self.robots[resource] + 1)

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

    def get_costs(self, robot_type):
        match robot_type:
            case "ore": return self.ore_robot_cost
            case "clay": return self.clay_robot_cost
            case "obsidian": return self.obsidian_robot_cost
            case "geode": return self.geode_robot_cost
            case _: raise "Unknown robot type, no cost map available"


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
