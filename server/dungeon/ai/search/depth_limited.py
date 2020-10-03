from .common import Node, NoSolutionError


def depth_limited_graph(problem, depth_limit, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    explored = set()
    iterations = 0
    depth_limited = False
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        if node.depth() < depth_limit:
            for action in problem.actions(node.state):
                child = node.get_child(problem, action)
                if (child.state not in explored and
                        child.state not in [n.state for n in frontier]):
                    if problem.goal_test(child.state):
                        return child.solution()
                    frontier.append(child)
        else:
            depth_limited = True
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError(depth_limited=depth_limited)


def depth_limited_tree(problem, depth_limit, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    depth_limited = False
    while frontier:
        node = frontier.pop()
        if node.depth() < depth_limit:
            for action in problem.actions(node.state):
                child = node.get_child(problem, action)
                if problem.goal_test(child.state):
                    return child.solution()
                frontier.append(child)
        else:
            depth_limited = True
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError(depth_limited=depth_limited)


def depth_limited_tree_check_path(problem, depth_limit, iteration_limit=10000):
    """
    Depth first tree search, but check the path to the current node
    for duplicate states.
    """
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    depth_limited = False
    while frontier:
        node = frontier.pop()
        if node.depth() < depth_limit:
            for action in problem.actions(node.state):
                child = node.get_child(problem, action)
                if child.state not in node.states_in_solution():
                    if problem.goal_test(child.state):
                        return child.solution()
                    frontier.append(child)
        else:
            depth_limited = True
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError(depth_limited=depth_limited)