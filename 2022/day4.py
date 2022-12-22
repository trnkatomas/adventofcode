
DEBUG = 0

def compute_intersections(fname):

    intersections = 0
    intersections_2 = 0

    def create_set(ranges):
        start = int(ranges.split("-")[0])
        end = int(ranges.split("-")[1])
        return set([i for i in range(start, end+1)])

    with open(fname) as infile:
        for line in infile:
            interval_1 = create_set(line.split(',')[0])
            interval_2 = create_set(line.split(',')[1])
            if DEBUG:
                print(line, end='\t')
                print(interval_1, interval_2)
            if interval_1.intersection(interval_2):
                if DEBUG:
                    print(interval_1.intersection(interval_2))
                intersections += 1
            if min(interval_2) <= min(interval_1) <= max(interval_2) or \
               min(interval_2) <= max(interval_1) <= max(interval_2) or \
               min(interval_1) <= min(interval_2) <= max(interval_1) or \
               min(interval_1) <= max(interval_2) <= max(interval_1):
                intersections_2 += 1
            else:
                print(line)
    assert intersections == intersections_2, f"{intersections} != {intersections_2}"
    return intersections


if __name__ == "__main__":
    intersections = compute_intersections("day4.small")
    print(intersections)

    intersections = compute_intersections("day4.input")
    print(intersections)