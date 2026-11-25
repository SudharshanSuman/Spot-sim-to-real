#!/usr/bin/env bash
# Train Spot staged curriculum in Isaac Lab (rsl_rl).
# usage: scripts/train.sh <isaaclab_dir> <stage1|stage2|rough> [num_envs]
# Stage 2 warm-starts from the stage-1 checkpoint named in its agent config (agent.yaml).
set -euo pipefail

ISAACLAB="${1:?usage: scripts/train.sh <isaaclab_dir> <stage1|stage2|rough> [num_envs]}"
STAGE="${2:?stage1|stage2|rough}"
NUM_ENVS="${3:-4096}"

case "$STAGE" in
  stage1) TASK=IsaacContrib-Velocity-Stage1-Spot ;;
  stage2) TASK=IsaacContrib-Velocity-Stage2-Spot ;;
  rough)  TASK=IsaacContrib-Velocity-Rough-Spot ;;
  *) echo "unknown stage: $STAGE" >&2; exit 1 ;;
esac

cd "$ISAACLAB"
# Training runs headless by default (visualizer: none); no --headless flag exists in this version.
./isaaclab.sh -p scripts/reinforcement_learning/train.py \
    --rl_library rsl_rl \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --seed 42
