#!/bin/bash
#SBATCH -C dgx -N 1
#SBATCH --gpus-per-node=2 --ntasks-per-node=1 --cpus-per-task=10 -t 6:00:00 -A nstaff


module load cgpu
module load cuda/11.0.2
module load cudnn/8.0.1
module load python
source activate emb

cd /global/cfs/cdirs/kbase/ke_prototype/KE_KG

EDGES="data/merged/merged_imgvr_mg_edges.tsv"
NODES="data/merged/merged_imgvr_mg_nodes.tsv"

OUT="merged_imgvr_mg"

srun python ./embeddings/Graph_node_emmbedding_using_SkipGram_generic.py $EDGES $NODES $OUT

