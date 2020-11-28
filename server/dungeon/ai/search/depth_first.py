from .common import Node, NoSolutionError


def depth_first_graph(problem, depth_limit=None, iteration_limit=10000):
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
        if node.depth == depth_limit:
            depth_limited = True
            continue
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
    raise NoSolutionError(iterations=iterations, depth_limited=depth_limited)


def depth_first_tree(problem, depth_limit=None, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = [starting_node]
    iterations = 0
    depth_limited = False
    while frontier:
        node = frontier.pop()
        if node.depth == depth_limit:
            depth_limited = True
            continue
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if problem.goal_test(child.state):
                return child.solution()
            frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations, depth_limited=depth_limited)


def depth_first_tree_check_path(problem, depth_limit=None,
                                iteration_limit=10000):
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
        if node.depth == depth_limit:
            depth_limited = True
            continue
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            if child.state not in node.states_in_solution():
                if problem.goal_test(child.state):
                    return child.solution()
                frontier.append(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations, depth_limited=depth_limited)


def depth_first_recursive(problem, depth_limit=None, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    return _find_solution(starting_node, problem, depth_limit, iteration_limit)


def _find_solution(node, problem, depth_limit, iteration_limit):
    if problem.goal_test(node.state):
        return node.solution()
    if depth_limit == 0:
        raise NoSolutionError(iterations=0, depth_limited=True)
    depth_limited = False
    iterations = 1
    for action in problem.actions(node.state):
        child = node.get_child(problem, action)
        try:
            return _find_solution(
                child, problem,
                depth_limit - 1 if depth_limit is not None else None,
                iteration_limit - iterations
            )
        except NoSolutionError as e:
            iterations += e.iterations
            if e.iteration_limited or iterations > iteration_limit:
                raise NoSolutionError(
                    iterations=iterations, iteration_limited=True)
            if e.depth_limited:
                depth_limited = True
    raise NoSolutionError(iterations=iterations, depth_limited=depth_limited)
