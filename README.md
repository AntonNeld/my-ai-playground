# ai-dungeon
Experimenting with AI and microservices.

## Getting started

Prerequisites:

```sh
pip3 install flask
pip3 install connexion
pip3 install requests
```

Try it out:

```sh
python3 dungeon/main.py
```

In another shell, do:

```sh
python3 text_client/main.py
```

## Docker stuff (future)

Install docker and set up a swarm:

```sh
sudo apt install docker.io
sudo usermod -aG docker ${USER}
# Log out and in again
docker swarm init
```

To be continued...