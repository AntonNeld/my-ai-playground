from .common import Node, NoSolutionError


def depth_first_graph(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    explored = set()
    iterations = 0
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if (child.state not in explored and
                    child.state not in [n.state for n in frontier]):
                if problem.goal_test(child.state):
                    return child.solution()
                frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError()


def depth_first_tree(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    while frontier:
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if problem.goal_test(child.state):
                return child.solution()
            frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError()


def depth_first_tree_check_path(problem, iteration_limit=10000):
    """
    Depth first tree search, but check the path to the current node
    for duplicate states.
    """
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    while frontier:
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if child.state not in node.states_in_solution():
                if problem.goal_test(child.state):
                    return child.solution()
                frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iteration_limit=iteration_limit)
    raise NoSolutionError()
