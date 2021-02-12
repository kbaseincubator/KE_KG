
tsv='./data/raw/imgvr/IMGVR_all_Sequence_information_InIMG-Yes_Linked-to_TaxonOIDs_v2_Completeness-50-100_nocol20_v1.tsv'

edge='./data/transform/imgvr_votu_sample/imgr_votu_sample_edges.tsv'
node='./data/transform/imgvr_votu_sample/imgr_votu_sample_nodes.tsv'



pairs = dict()
samples = dict()
otus = dict()
edges = ['subject	predicate	object	relation	provided_by']
nodes = ['id	name	category	provided_by']
predicate = 'biolink:occurs_in'
with open(tsv) as f:
    headers = None
    for line in f:
       ele=line.rstrip().split('\t')
       if ele[1]=='NA':
           continue
       if not headers:
           headers=ele
           continue
       votu = 'vOTU:' + ele[7].lower()
       gaid = 'GOLD:' + ele[1].lower()
       p = votu+':'+gaid
       if p not in pairs:
           l = [votu, predicate, gaid, predicate, 'GOLD']
           edges.append('\t'.join(l))
           pairs[p] = 1
       if votu not in otus:
           l = [votu, ele[7].lower(), 'kbase:otu', 'GOLD']
           nodes.append('\t'.join(l))
       if gaid not in samples:
           l = [gaid, gaid.replace('GOLD:',''), 'biolink:Attribute', 'GOLD']
           nodes.append('\t'.join(l))
      
      

with open(edge, 'w') as f:
    for e in edges:
        f.write(e+'\n')
with open(node, 'w') as f:
    for e in nodes:
        f.write(e+'\n')
