#!/bin/sh

PATH=/global/cfs/cdirs/kbase/ke_prototype/sw/R/bin:$PATH

[ -z "$EMB" ] && EMB=../../embeddings/SkipGram_merged_kg_embedding.tsv
[ -z "$NF" ] && NF=../../graphs/IMGVR/merged_kg_nodes.tsv

echo $EMB
echo $NF

cd /global/cfs/cdirs/kbase/ke_prototype/KE_KG/embeddings

../src/embeddings/query_by_similarity_cli.R -e  $EMB -n $NF -s $1

