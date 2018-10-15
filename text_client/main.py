import requests
import json

def main():
    while True:
        r = requests.get("http://127.0.0.1:5000/api/view")
        things = json.loads(r.text)
        print("-" * 7)
        for y in range(0, 6):
            line = "|"
            for x in range(0, 6):
                if [thing for thing in things if thing["x"] == x 
                                             and thing["y"] == y
                                             and thing["looks_like"] == "wall"]:
                    line += "#"
                else:
                    line += " "
            line += "|"
            print(line)
        print("-" * 7)
        input()

if __name__ == "__main__":
    main()