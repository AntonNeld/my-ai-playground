# ai-dungeon

Experimenting with AI and microservices. Very early phases so far.

## Getting started

Prerequisites:

* pipenv
* Add `export PIPENV_VENV_IN_PROJECT=1` to `.bashrc` or similar.

Install and use dependencies:

```sh
pipenv install --dev
pipenv shell
```

Try it out:

```sh
python dungeon/main.py
```

In another shell, do:

```sh
pipenv shell
python text_client/main.py
```
