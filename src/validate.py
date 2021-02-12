import sys

edge_nodes = dict()
nodes = dict()
merge_mode = False
header = False
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('id	'):
            merge_mode = True
        if not header:
            header=True
            continue
        if merge_mode:
           (id, sub, pred, obj, rel, pb) = line.split()
        else:
           (sub, pred, obj, rel, pb) = line.split()
        edge_nodes[sub] = 1
        edge_nodes[obj] = 1

header = False
with open(sys.argv[2]) as f:
    for line in f:
        if not header:
            header=True
            continue
        try:
           (id, cat, name, pb) = line.split()
        except:
           print("Bad node definition "+line)
        nodes[id] = 1

# Go through all the nodes
for n in nodes:
    if n not in edge_nodes:
        print("Extra node "+n)

for n in edge_nodes:
    if n not in nodes:
        print("Missing node "+n)
