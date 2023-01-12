def load_data(file):
    with open(f'input/{file}.txt') as f:
        return f.read().split('\n')


def process(data):
    sensor_beacon_pairs = []
    for d in data:
        [sensor, beacon] = d.split(':')
        [sensor_x, sensor_y] = sensor.replace('Sensor at ', '').split(',')
        sensor_coordinates = (int(sensor_x.replace('x=', '')), int(sensor_y.replace(' y=', '')))

        [beacon_x, beacon_y] = beacon.replace(' closest beacon is at ', '').split(',')
        beacon_coordinates = (int(beacon_x.replace('x=', '')), int(beacon_y.replace(' y=', '')))

        sensor_beacon_pairs.append((sensor_coordinates, beacon_coordinates))
    return sensor_beacon_pairs


def manhattan_distance(coord_a, coord_b):
    (ax, ay) = coord_a
    (bx, by) = coord_b

    return abs(bx - ax) + abs(by - ay)


def manhattan_chord_at_y(center_coord, manhattan_radius, target_y):
    """Returns the two points that intersect y from the given manhattan circle
    """

    (x, y) = center_coord
    delta_y = abs(target_y - y)
    if delta_y <= manhattan_radius:
        delta_x = manhattan_radius - delta_y
        return [(x - delta_x, target_y), (x + delta_x, target_y)]
    return []


def join_ranges(list_of_ranges):
    list_of_ranges = sorted(list_of_ranges)
    resulting_ranges = []
    current_accumulated_range = list_of_ranges[0]

    for current_range in list_of_ranges[1:]:
        ranges_touch = current_range[0] <= current_accumulated_range[1] + 1
        if ranges_touch:
            current_accumulated_range[1] = max(current_accumulated_range[1], current_range[1])
        else:
            resulting_ranges.append(current_accumulated_range)
            current_accumulated_range = current_range
    resulting_ranges.append(current_accumulated_range)
    return resulting_ranges


def ranges_covered(sensor_beacon_pairs, y_of_interest):
    ranges = []
    for sensor, beacon in sensor_beacon_pairs:
        x_range_covered = [coord[0] for coord in manhattan_chord_at_y(sensor,
                                                                      manhattan_distance(sensor, beacon),
                                                                      y_of_interest)]

        if x_range_covered:
            ranges.append(x_range_covered)

    return join_ranges(ranges)


if __name__ == '__main__':
    data = load_data('day_15')
    sensor_beacon_pairs = process(data)

    y_of_interest = 2000000
    ranges = ranges_covered(sensor_beacon_pairs, y_of_interest)

    beacon_x_locations = set()
    for _, beacon in sensor_beacon_pairs:
        (x, y) = beacon
        if y == y_of_interest:
            beacon_x_locations.add(x)
    beacon_x_iterator = iter(sorted(list(beacon_x_locations)))
    if beacon_x_locations:
        current_beacon = next(beacon_x_iterator)
    else:
        current_beacon = None
    total_covered_range = 0

    for current_range in join_ranges(ranges):
        beacons_inside_range = 0
        print(current_range)
        if current_beacon and current_range[0] <= current_beacon <= current_range[1]:
            beacons_inside_range += 1
            try:
                current_beacon = next(beacon_x_iterator)
            except StopIteration:
                current_beacon = None
        current_range_coverage = current_range[1] - current_range[0] + 1 - beacons_inside_range
        total_covered_range += current_range_coverage

    print(f"Part 1: there is a total of {total_covered_range} positions where a beacon cannot be present")

    for y in range(0, 4000000):
        ranges = ranges_covered(sensor_beacon_pairs, y)
        if len(ranges) > 1:
            x = int((ranges[0][1] + ranges[1][0]) / 2)
            print(f"Beacon location found at {(x, y)}")
            print(f"Tuning frequency: {x * 4000000 + y}")
