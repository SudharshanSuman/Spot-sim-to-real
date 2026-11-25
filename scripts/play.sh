#!/usr/bin/env bash
# Play a trained Spot policy (rsl_rl) in Isaac Lab.
# usage: scripts/play.sh <isaaclab_dir> [checkpoint.pt] [task] [num_envs]
# defaults: task=IsaacContrib-Velocity-Stage2-Spot, num_envs=16,
#           checkpoint=runs/spot_s2_final/model_29997.pt (not in git; see README)
set -euo pipefail

ISAACLAB="${1:?usage: scripts/play.sh <isaaclab_dir> [checkpoint.pt] [task] [num_envs]}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CKPT="${2:-$REPO/runs/spot_s2_final/model_29997.pt}"
TASK="${3:-IsaacContrib-Velocity-Stage2-Spot}"
NUM_ENVS="${4:-16}"

[ -f "$CKPT" ] || { echo "checkpoint not found: $CKPT" >&2; exit 1; }

cd "$ISAACLAB"
./isaaclab.sh -p scripts/reinforcement_learning/play.py \
    --rl_library rsl_rl \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --checkpoint "$(realpath "$CKPT")"
