from day_19 import MiningState, Blueprint

def default_blueprint():
    """Returns a default blueprint

    Costs are set high so we don't expect robots to be buyable
    within the alloted time.
    """
    return Blueprint(id=123, ore_robot_cost=500, clay_robot_cost=500,
              obsidian_ore_cost=500, obsidian_clay_cost=500,
              geode_ore_cost=500, geode_obsidian_cost=500)
def test_expect_to_wait_out_time():
    """Can't buy anything, just accumulate geodes"""
    blueprint = default_blueprint()
    state = MiningState(1,1,1,1,0,0,0,0,0)

    max_geodes = blueprint.dfs_max_geodes(state)
    expected = 25

    assert max_geodes == expected

def test_expect_to_buy_geode_robot():
    blueprint = Blueprint(123, 100, 100, 100, 100, 100, 100)
    state = MiningState(1, 1, 1, 1, 0, 0, 0, 0, 0)

    max_geodes = blueprint.dfs_max_geodes(state)
    expected = 25

    assert max_geodes == expected