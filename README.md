# spot-sim-to-real

Staged-curriculum reinforcement learning for a Boston Dynamics Spot quadruped in
[Isaac Lab](https://github.com/isaac-sim/IsaacLab) (rsl_rl PPO, manager-based velocity task).
Stage 1 trains on mixed terrain without stairs; stage 2 continues from the stage-1 policy.

This repo holds only the task configs, launch scripts, run parameters and logs metadata.
Checkpoints (`*.pt`) and the full Isaac Lab checkout are not included.

## Layout

| Path | What |
| --- | --- |
| `custom/` | Task configs: `stage1_env_cfg.py`, `stage2_env_cfg.py`, `rough_env_cfg.py`, the rsl_rl runner configs, and the gym registration `__init__.py`. |
| `scripts/install_tasks.sh` | Copies `custom/` into an Isaac Lab checkout. |
| `scripts/train.sh` | Train `stage1`, `stage2` or `rough`. |
| `scripts/play.sh` | Play a checkpoint. |
| `runs/spot_s2_final/` | Config snapshot (`params/agent.yaml`, `params/env.yaml`) and `run.json` for the stage-2 run used below. |

## Versions

Recorded on the machine that produced the runs.

| Component | Version |
| --- | --- |
| OS | Ubuntu 24.04.5 LTS, kernel 6.8.0-149-generic (x86_64) |
| GPU | NVIDIA GeForce RTX 4070, 12 GiB, sm_89 |
| NVIDIA driver | 595.99.02 |
| CUDA (as reported by Warp) | 12.9 |
| Python | 3.12.16 (uv-managed venv) |
| Isaac Sim | 6.2.0.0 (`isaacsim` pip package) |
| Isaac Lab | git `e3f7d9f` (upstream `main`) with the Spot task files from `custom/`; `VERSION` file reads `3.0.0`; installed packages `isaaclab` 28.0.0, `isaaclab_tasks` 25.2.0, `isaaclab_rl` 1.5.1 |
| rsl-rl-lib | 5.5.1 |
| Warp | 1.17.0 |
| Physics | `isaacsim_physx` (PhysX backend) |

## Reproduce

Prerequisites: an Isaac Lab installation that works on your machine (see the
[Isaac Lab Quickstart](https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/quickstart.html)),
and the Spot USD assets, which Isaac Lab downloads on first use.

```bash
# 1. Get the repo and an Isaac Lab checkout at the commit above
git clone https://github.com/<you>/spot-sim-to-real.git
git clone https://github.com/isaac-sim/IsaacLab.git
git -C IsaacLab checkout e3f7d9f
(cd IsaacLab && ./isaaclab.sh --install)

# 2. Install the Spot task configs into Isaac Lab
scripts/install_tasks.sh ./IsaacLab

# 3. Train (stage 1, then stage 2; stage 2 warm-starts from the stage-1 checkpoint)
scripts/train.sh ./IsaacLab stage1
scripts/train.sh ./IsaacLab stage2

# 4. Play a checkpoint (defaults to runs/spot_s2_final/model_29997.pt)
scripts/play.sh ./IsaacLab /path/to/model_XXXXX.pt
```

Checkpoint paths: put the stage-2 checkpoint at `runs/spot_s2_final/model_29997.pt`, or
pass its path as the second argument to `play.sh`. Stage 2 reads its warm-start checkpoint
from `agent.yaml` (`load_checkpoint`), which points at
`logs/rsl_rl/spot_s1/2026-11-25_00-50-55_s1_main/model_23998.pt`. Keep the stage-1 run
directory in place, or edit that line.

### Commands

These are the commands the scripts wrap, run from the Isaac Lab root. The stage-1 and
stage-2 training runs were launched with equivalent commands; their exact flags were not
recorded in this repo's sources, so `--seed 42` and `--num_envs 4096` come from the saved config.

```bash
./isaaclab.sh -p scripts/reinforcement_learning/train.py --rl_library rsl_rl --task IsaacContrib-Velocity-Stage1-Spot --num_envs 4096 --seed 42
./isaaclab.sh -p scripts/reinforcement_learning/train.py --rl_library rsl_rl --task IsaacContrib-Velocity-Stage2-Spot --num_envs 4096 --seed 42
./isaaclab.sh -p scripts/reinforcement_learning/play.py  --rl_library rsl_rl --task IsaacContrib-Velocity-Stage2-Spot --num_envs 16 --checkpoint <path-to>/model_29997.pt
```

Notes:
- Training runs headless by default (visualizer: none). The `--headless` flag is not
  accepted by these scripts in this Isaac Lab version.
- `play.py` needs `--rl_library rsl_rl`.

### Checkpoint used

Stage 2, run `2026-11-25_09-23-42_s2_main`, final checkpoint `model_29997.pt`. It is the last
checkpoint saved, not necessarily the one with the highest reward. Play was run with the
exact command above. The policy loaded and ran without errors (the test was stopped by a
timeout, since play runs until interrupted).

## Status

- Training and play run on the machine listed above.
- Stage-1 final checkpoint: `model_23998.pt` (run `2026-11-25_00-50-55_s1_main`).
- Stage-2 final checkpoint: `model_29997.pt` (run `2026-11-25_09-23-42_s2_main`).
- Not included: checkpoints, tensorboard event files, raw text logs (about 56 MB).

## Not in this repo

`custom/` depends on upstream Isaac Lab for the base Spot flat task (`flat_env_cfg.py`,
`rsl_rl_ppo_cfg.py`) and the Spot assets. `install_tasks.sh` does not copy those.

## License

Not yet chosen. Isaac Lab itself is BSD-3-Clause.
