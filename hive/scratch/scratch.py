import json

def fizzBuzz():
    # lines = ["[", "[", "a"]
    j = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    p = json.loads('"{1:4}"')
    z = j.append(p)
    j.append({"apps":32})

    print(f"{j}")
    # Write your code here


if __name__ == '__main__':
    # f = float("32.34")

    print(f"{b}, {type(b)}")
