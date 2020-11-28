class NoSolutionError(Exception):

    def __init__(self, iterations, depth_limited=False,
                 iteration_limited=False):
        self.iterations = iterations
        self.iteration_limited = iteration_limited
        self.depth_limited = depth_limited


class Node:

    def __init__(self, state, path_cost, parent=None, action=None):
        self.state = state
        self.path_cost = path_cost
        self.parent = parent
        self.action = action
        self.depth = parent.depth + 1 if parent is not None else 0

    def get_child(self, problem, action):
        state = problem.result(self.state, action)
        path_cost = (
            self.path_cost + problem.step_cost(self.state, action, state)
        )
        return Node(state, path_cost, parent=self, action=action)

    def solution(self):
        if self.parent is None:
            return []
        return self.parent.solution() + [self.action]

    def states_in_solution(self):
        if self.parent is None:
            return [self.state]
        return self.parent.states_in_solution() + [self.state]

    def depth(self):
        return self.depth
