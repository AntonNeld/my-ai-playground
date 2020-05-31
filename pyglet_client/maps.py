import uuid

import pytmx


def load(path, player_ai):
    things = []
    tiledata = pytmx.TiledMap(path)
    for layer in tiledata.layers:
        thing_type = layer.properties["Type"]
        for (x, inverted_y, gid) in layer.iter_data():
            y = tiledata.height - inverted_y - 1
            if gid != 0:
                thing = {"type": thing_type, "x": x, "y": y}
                if thing_type == "player":
                    thing["ai"] = player_ai
                things.append(thing)
    return {"entities": {uuid.uuid4().hex: thing for thing in things}}
