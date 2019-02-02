import draw
import requests
import json


def main():
    drawer = draw.Draw()

    while True:
        r = requests.get("http://127.0.0.1:5000/api/view")
        things = json.loads(r.text)
        print(things)
        drawer.draw()
        input()
        r = requests.post("http://127.0.0.1:5000/api/step")


if __name__ == "__main__":
    main()
