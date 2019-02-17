
def breadth_first(origin, destination, obstructions):
    frontier = set([origin])
    steps = find_steps(frontier, set(), obstructions, destination)
    if not steps:
        return ["none"]
    actions = []
    last_location = steps.pop(0)
    while steps:
        next_location = steps.pop(0)
        dx = next_location[0] - last_location[0]
        dy = next_location[1] - last_location[1]
        if dx == 1:
            actions.append("move_right")
        elif dx == -1:
            actions.append("move_left")
        elif dy == 1:
            actions.append("move_up")
        elif dy == -1:
            actions.append("move_down")
        last_location = next_location
    return actions


def find_steps(frontier, explored, obstructions, destination):
    if destination in frontier:
        return [destination]
    if not frontier:
        return None
    new_explored = explored.union(frontier)
    new_frontier = set()
    for node in frontier:
        for new_node in adjacent(node):
            if not (new_node in new_explored or new_node in obstructions):
                new_frontier.add(new_node)
    steps = find_steps(new_frontier, new_explored, obstructions, destination)
    if not steps:
        return None
    for node in adjacent(steps[0]):
        if node in frontier:
            return [node] + steps


def adjacent(node):
    x, y = node
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
