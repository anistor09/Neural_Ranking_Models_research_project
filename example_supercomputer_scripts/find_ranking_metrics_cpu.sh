#!/bin/bash

#SBATCH --job-name="cpu_metrics_e5_base"
#SBATCH --time=05:00:00
#SBATCH --partition=compute-p2 # GPU is not needed anything runs with CUDA
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=90G # High RAM memory usage because of the big MS MARCO indexes that are loaded in memory
#SBATCH --account=Education-EEMCS-Courses-CSE3000

module load 2023r1
module load python
module load py-pip
module load openjdk
module load cuda


export IR_DATASETS_SKIP_DISK_FREE=true
export IR_DATASETS_HOME=/scratch/anistor/.ir_datasets/


# Install dependencies
python -m pip install --user python-terrier==0.10.0 fast-forward-indexes==0.2.0 jupyter ipywidgets transformers typing pathlib func-timeout



# Run the experiment
srun python -m e5.experiments.ranking_measures_e5_base > ranking_measures_e5_base_status.txt

