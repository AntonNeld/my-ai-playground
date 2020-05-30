# ai-dungeon

Experimenting with AI and web development. Very early phases so far, no actual AI included.

The philosophy is to have a RESTful (with exceptions) backend, and going back to the basics in the frontend.

## Getting started

Prerequisites:

- [pipenv](https://pypi.org/project/pipenv/)
- Add `export PIPENV_VENV_IN_PROJECT=1` to `.bashrc` or similar. Or don't, your choice.
- [tiled](https://www.mapeditor.org/), if you want to make new maps.

Install and use dependencies:

```sh
pipenv install --dev
pipenv shell
```

Run the backend:

```sh
cd server
uvicorn main:app --port 8300 --reload
```

### pyglet frontend (to be deprecated)

In another shell, connect with the scenario using the frontend:

```sh
pipenv shell
python pyglet_client/main.py <PATH_TO_MAP>
```

Instructions will be printed in the terminal.

To use a different AI than the default, set the environment variable PLAYER_AI to the service name when starting the client. Default is `pathfinder`.

### Web frontend

In a web browser, connect to `localhost:8300`.

### Testing

In another shell, run:

```sh
pipenv shell
pytest
```

There is no CI, I just try to remember doing it before committing.

## Creating new maps

Create a new map using Tiled. Each type of object should have its own layer, with a custom property `Type` signifying what it is.
