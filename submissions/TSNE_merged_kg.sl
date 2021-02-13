#!/bin/bash

#SBATCH -C dgx -N 1 
#SBATCH --gpus-per-node=1 --ntasks-per-node=1 --cpus-per-task=10 -t 4:00:00 -A nstaff

#module load  cuda/11.0.2
#module load python
#source activate emb
PATH=/global/common/software/kbase/python3/bin:$PATH

cd /global/cfs/cdirs/kbase/ke_prototype/KE_KG

RUN=merged_kg

EMB=../embeddings/SkipGram_${RUN}_embedding.npy
EDGE=./data/merged/${RUN}_edges.tsv
NODE=./data/merged/${RUN}_nodes.tsv


srun python ./embeddings/TSNE_node_types_visualization_generic.py $EMB $EDGE $NODE $RUN

