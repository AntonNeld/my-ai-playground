import connexion
import os
from os.path import abspath, dirname, join
import room

if "DUNGEON_MAP" in os.environ:
    MAP = os.environ["DUNGEON_MAP"]
else:
    MAP = "default"

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

if __name__ == "__main__":
    room.set_current_room(room.create_room_from_tilemap(
        join(dirname(abspath(__file__)), "maps", MAP + ".tmx")))
    app.run(host="0.0.0.0", port=5000, debug=True)
