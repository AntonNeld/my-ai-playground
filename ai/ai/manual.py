
actions = {}


def next_move(agent, percept):
    try:
        return actions[agent]
    except KeyError:
        return "none"


def set_move(agent, action):
    actions[agent] = action


def delete(agent):
    if agent in actions:
        del actions[agent]
