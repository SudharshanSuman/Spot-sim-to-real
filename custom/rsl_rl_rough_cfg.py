from isaaclab.utils import configclass

from .rsl_rl_ppo_cfg import SpotFlatPPORunnerCfg


@configclass
class SpotRoughPPORunnerCfg(SpotFlatPPORunnerCfg):
    experiment_name = "spot_rough"
    max_iterations = 3000
