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
python text_client/main.py
```

Press any key to advance the world one step. If the scenario is `manual.yml` the arrow keys control the player.