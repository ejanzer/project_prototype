from sys import argv

def dedupe(source, target):
    with open(source, 'r') as f:
        data = f.readlines()

    w = open(target, 'w')

    visited = {}

    for dish in data:
        if visited.get(dish):
            pass
        else:
            visited[dish] = True
            w.write(dish)

    w.close()

if __name__ == "__main__":
    script, source, target = argv
    dedupe(source, target)