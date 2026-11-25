#!/usr/bin/env bash
# Copy the Spot staged-training task configs from this repo into an Isaac Lab checkout.
# usage: scripts/install_tasks.sh /path/to/IsaacLab
set -euo pipefail

ISAACLAB="${1:?usage: scripts/install_tasks.sh /path/to/IsaacLab}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ISAACLAB/source/isaaclab_tasks/isaaclab_tasks/contrib/velocity/config/spot"

[ -d "$DEST" ] || { echo "not an Isaac Lab checkout: $DEST missing" >&2; exit 1; }

mkdir -p "$DEST/agents"
cp "$REPO"/custom/__init__.py "$DEST/__init__.py"
cp "$REPO"/custom/rough_env_cfg.py "$REPO"/custom/stage1_env_cfg.py "$REPO"/custom/stage2_env_cfg.py "$DEST/"
cp "$REPO"/custom/rsl_rl_rough_cfg.py "$REPO"/custom/rsl_rl_stage_cfg.py "$DEST/agents/"
echo "Installed Spot task configs into $DEST"
