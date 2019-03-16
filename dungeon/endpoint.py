import rooms

# Get stuff.


def get_view(room):
    return rooms.get_room(room).get_view(include_id=True)


def get_score(room, agents=None):
    scores = []
    for agent in rooms.get_room(room).get_agents():
        if agents is None or agent in agents:
            scores.append({"id": agent.id, "score": agent.score})
    return scores


def get_steps(room):
    return rooms.get_room(room).steps


def step(room):
    rooms.get_room(room).step()


def create_room(room):
    rooms.init_room(room)


def delete_room(room):
    rooms.delete_room(room)
