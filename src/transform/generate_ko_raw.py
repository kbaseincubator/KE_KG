#!/usr/bin/python
# Read eggnog annotations and create
# a collapsed edge with one edge per metagenome ID 
# to Kegg ID.  Also prints out the number of occurences,
# the total number of features for the metagenome and
# all of the contigs the term appears in for that metagenomes.
# The last also has includes the number of other kegg terms
# for that feature.

import sys

samples = dict()
last = ''
samples[last] = dict()

tot = 0
ko_contigs = dict()
of=open('kos.tsv', 'w')
of.write("#mg_id\tKO_Term\tko_count\ttotal\tcontigs_list\n")
for line in sys.stdin:
    if line[0]=='#':
       continue
    list = line.split('\t')
    sam = list[0].split('_')[0]
    if sam!=last:
        ct = 0
        print(last)
        for ko in samples[last].keys():
             of.write('%s\t%s\t %d\t %d\t%s\n' %(last, ko, samples[last][ko], tot, ','.join(ko_contigs[ko])))
             ct += 1
#        print(last, samples[last])
        last = sam
        samples[sam] = dict()
        tot = 0
        ko_contigs = dict()
    tot += 1
    if list[8]=='':
        continue
#    print(sam,list[8])
    ko_terms = list[8].split(',')
    for ko in ko_terms:
        if ko not in samples[sam]:
            samples[sam][ko]=0
        if ko not in ko_contigs:
            ko_contigs[ko] = []
        samples[sam][ko]+=1
        ko_contigs[ko].append('%s:%d' % (list[0], len(ko_terms)))
