#!/bin/bash


#SBATCH --cpus-per-task=8
#SBATCH --gpus=1
#SBATCH --mem=80G
#SBATCH --time=00:10:00
#SBATCH --mail-user=tung.bui@aalto.fi
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END



export HF_HOME="/scratch/work/buit8"
source activate text-image-env

cd /scratch/work/buit8

python text-video-v5.py        

python merge-image-music-v1.py 