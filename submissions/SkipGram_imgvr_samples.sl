#!/bin/bash
#SBATCH -C dgx -N 1
#SBATCH --gpus-per-node=2 --ntasks-per-node=1 --cpus-per-task=10 -t 6:00:00 -A nstaff


module load cgpu
module load cuda/11.0.2
module load cudnn/8.0.1
module load python
source activate emb

cd /global/cfs/cdirs/kbase/ke_prototype/KE_KG

EDGES="data/transform/imgvr/IMGVR_sample_KGX_edges.tsv"

OUT="imgvr_samples"

srun python ./embeddings/Graph_node_emmbedding_using_SkipGram_generic.py $EDGES $OUT

