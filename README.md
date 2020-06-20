# ai-dungeon

Experimenting with AI and web development. Very early phases so far, no actual AI included.

The philosophy is to have a RESTful (with exceptions) backend, and going back to the basics in the frontend.

## Getting started

Prerequisites:

- [pipenv](https://pypi.org/project/pipenv/)
- Add `export PIPENV_VENV_IN_PROJECT=1` to `.bashrc` or similar. Or don't, your choice.

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

In a web browser, connect to `localhost:8300`.

## Testing

Run:

```sh
pipenv shell
pytest
```

The server does not need to be running for this. There is no CI, I just try to remember doing it before committing.
