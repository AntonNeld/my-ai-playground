from .common import Node, NoSolutionError


def breadth_first_graph(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    explored = set()
    iterations = 0
    while frontier:
        node = frontier.pop(0)
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
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations)


def breadth_first_tree(problem, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    while frontier:
        node = frontier.pop(0)
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if problem.goal_test(child.state):
                return child.solution()
            frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations)
