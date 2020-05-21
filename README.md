# ai-dungeon

Experimenting with AI. Very early phases so far.

## Getting started

Prerequisites:

- [pipenv](https://pypi.org/project/pipenv/)
- Add `export PIPENV_VENV_IN_PROJECT=1` to `.bashrc` or similar.
- [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [tiled](https://www.mapeditor.org/), if you want to make new maps.

Install and use dependencies:

```sh
pipenv install --dev
pipenv shell
```

Run the backend:

```sh
docker-compose -f compose.yml up --build
```

### pyglet frontend

In another shell, connect with the scenario using the frontend:

```sh
pipenv shell
python pyglet_client/main.py <PATH_TO_MAP>
```

Instructions will be printed in the terminal.

To use a different AI than the default, set the environment variable PLAYER_AI to the service name when starting the client. Default is `pathfinder`. (This config will change soon.)

### Testing

In another shell, run:

```sh
pipenv shell
pytest
```

Do this before committing

## Creating new maps

Create a new map using Tiled. Each type of object should have its own layer, with a custom property `Type` signifying what it is.

## Creating new AIs

Add a file `<AI name>.py` under `dungeon/ais/`, containing the functions `next_move(agent, percept)` and `delete(agent)`.
