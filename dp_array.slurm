#!/bin/bash

#SBATCH --job-name=dp_extract
#SBATCH --output=logs/dp_%A_%a.out
#SBATCH --error=logs/dp_%A_%a.err
#SBATCH --time=00:05:00
#SBATCH --mem=6G
#SBATCH --cpus-per-task=1
#SBATCH --account=tommy
#SBATCH --partition=standard
#SBATCH --qos=standard


# Activate your Python environment here
source activate tommy_ukmo_conda_2

TASK_ID=$((TASK_OFFSET + SLURM_ARRAY_TASK_ID))

read RADAR YEAR DAY TIME <<< $(python get_task.py "$TASK_ID")

echo "Radar: $RADAR"
echo "Year: $YEAR"
echo "Day: $DAY"
echo "Time: $TIME"

# Read processing parameters from config.py
eval "$(python -c '
from config import rmin, rmax, eles
print(f"RMIN={rmin}")
print(f"RMAX={rmax}")
print("ELES=" + ",".join(map(str, eles)))
')"

python dp_main.py \
    -r "$RADAR" \
    -y "$YEAR" \
    -d "$DAY" \
    -t "$TIME" \
    -rmin "$RMIN" \
    -rmax "$RMAX" \
    -e "$ELES"

echo "Finished task $TASK_ID"