#!/usr/bin/python

import sys

samples = dict()
last = ''
samples[last] = dict()

vid2id = dict()

with open('IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1_vOTU-reps.tsv') as f:
    for line in f:
        ele=line.split('\t')
        vid2id[ele[2]] = ele[7]
        

tot = 0
ko_contigs = dict()
of=open('kos.tsv', 'w')
of.write("#mg_id\tKO_Term\tko_count\ttotal\tcontigs_list\n")

for line in sys.stdin:
    if line[0]=='#':
       continue
    list = line.split('\t')
    vid = list[0].split('|')[0]
    sam = 'vOTU:%s' % (vid2id[vid].lower())
    if sam!=last:
        ct = 0
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
