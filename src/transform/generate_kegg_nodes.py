#!/usr/bin/python
# 
# Usage: cat out.tsv|cut -f 3 |sort|uniq | \
#             grep ko:|python ./generate_kegg_nodes.py
#
#
import sys

print("id	name	category	provided_by")

for line in sys.stdin:
    k=line.rstrip()
    print("%s\t%s\tbiolink:Function\tEggNog" % (k, k))

