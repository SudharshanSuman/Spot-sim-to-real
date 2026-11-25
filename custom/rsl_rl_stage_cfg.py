from isaaclab.utils import configclass

from .rsl_rl_ppo_cfg import SpotFlatPPORunnerCfg


@configclass
class SpotStage1PPORunnerCfg(SpotFlatPPORunnerCfg):
    experiment_name = "spot_s1"
    max_iterations = 4000


@configclass
class SpotStage2PPORunnerCfg(SpotFlatPPORunnerCfg):
    experiment_name = "spot_s2"
    max_iterations = 6000
