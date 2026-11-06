#!/bin/bash

mkdir -p logs

TOTAL_TASKS=$(python get_task.py --count)

CHUNK_SIZE=$(python -c "from config import chunk_size; print(chunk_size)")
MAX_CONCURRENT=$(python -c "from config import max_concurrent; print(max_concurrent)")

echo "Total tasks: $TOTAL_TASKS"
echo "Maximum concurrent jobs: $MAX_CONCURRENT"

for ((START=0; START<TOTAL_TASKS; START+=CHUNK_SIZE))
do

    END=$((START + CHUNK_SIZE - 1))

    if [ "$END" -ge "$TOTAL_TASKS" ]; then
        END=$((TOTAL_TASKS - 1))
    fi

    ARRAY_END=$((END - START))

    echo "Submitting tasks $START to $END"

    sbatch \
        --array=0-${ARRAY_END}%${MAX_CONCURRENT} \
        --export=ALL,TASK_OFFSET=$START \
        dp_array.slurm

done

echo "All jobs submitted"