import room

# Get stuff.


def get_view():
    return room.get_current_room().get_view(include_id=True)


def get_score(agents=None):
    scores = []
    for agent in room.get_current_room().get_agents():
        if agents is None or agent in agents:
            scores.append({"id": agent.id, "score": agent.score})
    return scores


def get_steps():
    return room.get_current_room().steps


def step():
    room.get_current_room().step()


def reset():
    room.init_room()
