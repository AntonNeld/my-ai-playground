# ai-dungeon

Experimenting with AI and microservices. Very early phases so far.

## Getting started

Prerequisites:

* [pipenv](https://pypi.org/project/pipenv/)
* Add `export PIPENV_VENV_IN_PROJECT=1` to `.bashrc` or similar.
* [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [tiled](https://www.mapeditor.org/), if you want to make new maps.

Install and use dependencies:

```sh
pipenv install --dev
pipenv shell
```

Run a scenario:

```sh
docker-compose -f scenarios/random-movement.yml up --build
```

In another shell, connect with the scenario using the frontend:

```sh
pipenv shell
python pyglet_client/main.py <PATH_TO_MAP>
```

## Using the frontend

If you use the `manual` AI (like in the scenario `manual`), you can control the player with the arrow keys.

Press R to reset the dungeon.

Any other key steps the world one step forward.

## Creating new scenarios

Create a new `.yml` file in `scenarios`. For many purposes, it's enough to copy `random-movement.yml` and changing:

* `build` and `volumes` in `ai`, to another AI placed in `ai`.

## Creating new maps

Create a new map using Tiled. Each type of object should have its own layer, with a custom property `Type` signifying what it is.

## Creating new AIs

Copy `ai/ai_skeleton`, and change `next_move(state)` in `endpoint.py`. It should examine `state` and return one of `"none"`,`"move_left"`,`"move_right"`,`"move_up"`,`"move_down"`.