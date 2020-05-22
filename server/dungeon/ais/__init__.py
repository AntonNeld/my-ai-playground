import importlib
import os
from os import path

# Dynamically import all modules from ai/ into ai_types
ai_types = {}
for f in os.listdir(path.dirname(__file__)):
    module = f.replace(".py", "")
    if module != "__init__":
        ai_types[module] = importlib.import_module(
            "dungeon.ais.{}".format(module))
