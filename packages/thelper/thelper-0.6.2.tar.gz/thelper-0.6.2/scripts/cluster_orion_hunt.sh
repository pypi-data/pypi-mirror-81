#!/bin/bash
#SBATCH --job-name=thelper-orion
#SBATCH --partition=main
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:24gb:1
#SBATCH --mem-per-cpu=4gb
#SBATCH --time=4:00:00
#SBATCH --output=sessions/orion/logs/%A_%a.log
#SBATCH --error=sessions/orion/logs/%A_%a.log
#SBATCH --array=1-80%2

echo    "Arguments: $@"
echo -n "Date:      "; date
echo    "JobId:     $SLURM_JOBID"
echo    "TaskId:    $SLURM_ARRAY_TASK_ID"
echo    "JobName:   $SLURM_JOB_NAME"
echo    "Node:      $HOSTNAME"
echo    "Nodelist:  $SLURM_JOB_NODELIST"

export PYTHONUNBUFFERED=1
module purge
module load cuda/10.0/cudnn/7.6
module load miniconda/3
source $CONDA_ACTIVATE
conda activate thelper

export ORION_DB_ADDRESS='sessions/orion/database.pkl'
export ORION_DB_TYPE='pickleddb'

"$CONDA_PREFIX/bin/orion" hunt \
    --config configs/orion.yml \
    --worker-trials 1 \
    --working-dir 'sessions/orion' \
    "$CONDA_PREFIX/bin/python" thelper/cli.py new \
        --config 'configs/agrivis-ae.yml' \
        --save-dir 'sessions/orion/thelper_{trial.id}/'
