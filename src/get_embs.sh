#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpu-bind=closest
#SBATCH --gpus=1
#SBATCH --output=/clusterusers/furkan.akkurt@boun.edu.tr/58t-app/outs/%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=furkanakkurt9285@gmail.com
#SBATCH --mem=200GB
#SBATCH -t 14-00:00

/clusterusers/furkan.akkurt@boun.edu.tr/58t-app/.venv/bin/python3 /clusterusers/furkan.akkurt@boun.edu.tr/58t-app/src/get_embs.py

RET=$?

exit $RET
