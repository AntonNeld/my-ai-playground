import connexion
import room

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

if __name__ == "__main__":
    room.set_current_room(room.create_room_from_tilemap("dungeon/map.tmx"))
    app.run(host="0.0.0.0", port=5000, debug=True)
