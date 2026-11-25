"""Spot staged terrain training (blind policy). Stage 1: terrain variety, no stairs."""

import isaaclab.terrains as terrain_gen
from isaaclab.utils import configclass

from .flat_env_cfg import SpotFlatEnvCfg

STAGE1_TERRAIN_CFG = terrain_gen.TerrainGeneratorCfg(
    size=(8.0, 8.0),
    border_width=20.0,
    num_rows=10,
    num_cols=20,
    horizontal_scale=0.1,
    vertical_scale=0.005,
    slope_threshold=0.75,
    difficulty_range=(0.0, 1.0),
    curriculum=True,
    use_cache=False,
    sub_terrains={
        "flat": terrain_gen.MeshPlaneTerrainCfg(proportion=0.1),
        "random_rough": terrain_gen.HfRandomUniformTerrainCfg(
            proportion=0.15, noise_range=(0.02, 0.06), noise_step=0.02, border_width=0.25
        ),
        "slope_up": terrain_gen.HfPyramidSlopedTerrainCfg(
            proportion=0.2, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
        "slope_down": terrain_gen.HfInvertedPyramidSlopedTerrainCfg(
            proportion=0.2, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
        "waves": terrain_gen.HfWaveTerrainCfg(
            proportion=0.2, amplitude_range=(0.01, 0.08), num_waves=4, border_width=0.25
        ),
        "obstacles": terrain_gen.HfDiscreteObstaclesTerrainCfg(
            proportion=0.15, obstacle_height_mode="choice", obstacle_width_range=(0.4, 1.0),
            obstacle_height_range=(0.03, 0.12), num_obstacles=40, platform_width=2.0, border_width=0.25
        ),
    },
)


@configclass
class SpotStage1EnvCfg(SpotFlatEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.terrain.terrain_generator = STAGE1_TERRAIN_CFG
        self.scene.terrain.max_init_terrain_level = 2
