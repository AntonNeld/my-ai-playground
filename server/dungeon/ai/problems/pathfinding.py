class PathfindingProblem:

    def __init__(self, start, goals, obstacles, penalties):
        self.start = start
        self.goals = goals
        self.obstacles = obstacles
        self.penalties = penalties

    def initial_state(self):
        return self.start

    def actions(self, state):
        actions = []
        x = state[0]
        y = state[1]
        if (x, y+1) not in self.obstacles:
            actions.append("move_up")
        if (x, y-1) not in self.obstacles:
            actions.append("move_down")
        if (x+1, y) not in self.obstacles:
            actions.append("move_right")
        if (x-1, y) not in self.obstacles:
            actions.append("move_left")
        return actions

    def result(self, state, action):
        x = state[0]
        y = state[1]
        if action == "move_up":
            return (x, y+1)
        if action == "move_down":
            return (x, y-1)
        if action == "move_right":
            return (x+1, y)
        if action == "move_left":
            return (x-1, y)
        return (x, y)

    def goal_test(self, state):
        return state in self.goals

    def step_cost(self, state, action, result):
        if result in self.penalties:
            return 1 + self.penalties[result]
        return 1


def get_heuristic(problem):
    def heuristic(node):
        distances = [abs(goal[0] - node.state[0]) +
                     abs(goal[1] - node.state[1]) for goal in problem.goals]
        return min(distances)
    return heuristic
