import rooms

# Get stuff.


def get_view(room):
    return rooms.get_current_room().get_view(include_id=True)


def get_score(room, agents=None):
    scores = []
    for agent in rooms.get_current_room().get_agents():
        if agents is None or agent in agents:
            scores.append({"id": agent.id, "score": agent.score})
    return scores


def get_steps(room):
    return rooms.get_current_room().steps


def step(room):
    rooms.get_current_room().step()


def reset(room):
    rooms.init_room()
