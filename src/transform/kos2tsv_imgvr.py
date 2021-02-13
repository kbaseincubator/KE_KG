#!/usr/bin/env python
#
# Input: results from generate_ko_edges.py
#
import sys

input = sys.argv[1]
edge_file = sys.argv[2]
node_file = sys.argv[3]


edges = open(edge_file, 'w')
edges.write('subject	predicate	object	relation	provided_by\n')

edge_label = 'kbase:has_function'
provided_by = 'eggnog'

unique_kos = dict()
goldids = dict()
pairs = dict()
with open(input) as f:
    for line in f:
        (subject, ko) = line.rstrip().split('\t')[0:2]
        rec =[subject, edge_label, ko, edge_label, provided_by]
        pair = subject+ko
        unique_kos[ko] = 1
        goldids[subject] = 1
        line = "%s\n" % ('\t'.join(rec))
        # avoid dups
        if pair not in pairs:
            edges.write(line)
            pairs[pair] = 1


nodes = open(node_file, 'w')
print("Writing Nodes")
nodes.write('id	name	category	provided_by\n')
for ko in unique_kos.keys():
    rec = [ko, ko, 'biolink:Function','EggNog']
    line = "%s\n" % ('\t'.join(rec))
    nodes.write(line)

# First visisted is None
for id in goldids.keys():
    rec = [id, id.replace('vOTU:', ''), 'kbase:otu','GOLD']
    line = "%s\n" % ('\t'.join(rec))
    nodes.write(line)

