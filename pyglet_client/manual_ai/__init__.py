import connexion
import threading
from . import endpoint

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


def run():
    kwargs = {"host": "0.0.0.0", "port": 5100, "debug": False}
    thread = threading.Thread(target=app.run, kwargs=kwargs)
    thread.start()


def set_action(action):
    endpoint.CURRENT_ACTION = action
