class NoSolutionError(Exception):

    def __init__(self, iteration_limit=None):
        self.iteration_limit = iteration_limit


class Node:

    def __init__(self, state, path_cost, parent=None, action=None):
        self.state = state
        self.path_cost = path_cost
        self.parent = parent
        self.action = action

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
