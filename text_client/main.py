import requests
import json

SYMBOLS = {"wall": "#"}
DEFAULT_SYMBOL = "?"


def print_field(things):
    print("-" * 8)
    for y in range(0, 6):
        line = "|"
        for x in range(0, 6):
            things_here = [thing for thing in things if thing["x"] == x
                           and thing["y"] == y]
            if things_here:
                thing = things_here[0]["looks_like"]
                if thing in SYMBOLS:
                    line += SYMBOLS[thing]
                else:
                    line += DEFAULT_SYMBOL
            else:
                line += " "
        line += "|"
        print(line)
    print("-" * 8)


def main():
    while True:
        r = requests.get("http://127.0.0.1:5000/api/view")
        things = json.loads(r.text)
        print(things)
        print_field(things)
        input()
        r = requests.post("http://127.0.0.1:5000/api/step")


if __name__ == "__main__":
    main()
