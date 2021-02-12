#!/usr/bin/env python
#
# Input: results from generate_ko_edges.py
#
# Uses Map files to convert from Torben's ID space to 
# GOLD Ga IDs.
import sys

input = sys.argv[1]
edge_file = sys.argv[2]
node_file = sys.argv[3]


imgid2ga = dict()
base = '/global/cfs/cdirs/kbase/ke_prototype/graphs/Torben/'
with open(base + 'IMG_TaxonOID_to_GOLD_Analysis_ID_v1.tsv') as f:
    for line in f:
        (tid, ga) = line.rstrip().split(' ')
        imgid2ga[tid] = ga

torb2img = dict()
meta = dict()
fields = [10, 11, 12, 13, 18, 19]
with open(base + 'Torben_IMG-data_linked_to-GOLD_v2.tsv') as f:
    for line in f:
        #print(line)
        (tid, imgid) = line.rstrip().split('\t')[0:2]
        if imgid in imgid2ga:
            # print(tid,imgid2ga[imgid])
            torb2img[tid] = 'GOLD:' + imgid2ga[imgid].lower()
            meta[tid] = line.rstrip().split('\t')


edges = open(edge_file, 'w')
edges.write('subject	predicate	object	relation	provided_by\n')

edge_label = 'kbase:has_function'
provided_by = 'eggnog'

unique_kos = dict()
goldids = dict()
pairs = dict()
with open(input) as f:
    for line in f:
        (tid, ko) = line.rstrip().split('\t')[0:2]
        if tid in torb2img:
            subject = torb2img[tid]
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
    rec = [id, id.replace('GOLD:', ''), 'biolink:Attribute','GOLD']
    line = "%s\n" % ('\t'.join(rec))
    nodes.write(line)

