# ai-dungeon
Experimenting with AI and microservices.

## Getting started

Prerequisites:

```sh
pip3 install flask
pip3 install connexion
```

Try it out:

```sh
python3 dungeon/main.py
```

In a web browser, go to:

```
localhost:5000/api/sheep
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