from sortedcontainers import SortedList

from .common import Node, NoSolutionError


def a_star_graph(problem, heuristic, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = SortedList([starting_node], key=lambda n: -
                          (n.path_cost + heuristic(n)))
    explored = set()
    iterations = 0
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node.solution()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            child_in_frontier = child.state in [n.state for n in frontier]
            if (child.state not in explored and not child_in_frontier):
                frontier.add(child)
            elif child_in_frontier:
                index = [n.state for n in frontier].index(child.state)
                other_node = frontier[index]
                if child.path_cost < other_node.path_cost:
                    frontier.remove(other_node)
                    frontier.add(child)

        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations)


def a_star_tree(problem, heuristic, iteration_limit=10000):
    starting_node = Node(problem.initial_state(), 0)
    if problem.goal_test(starting_node.state):
        return starting_node.solution()
    frontier = SortedList([starting_node], key=lambda n: -
                          (n.path_cost + heuristic(n)))
    iterations = 0
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node.solution()
        for action in problem.actions(node.state):
            child = node.get_child(problem, action)
            frontier.add(child)
        iterations += 1
        if iterations > iteration_limit:
            raise NoSolutionError(iterations=iterations,
                                  iteration_limited=True)
    raise NoSolutionError(iterations=iterations)
