"""Spot rough-terrain task (stairs + slopes + bumps), blind policy. Derived from the contrib flat task."""

import isaaclab.terrains as terrain_gen
from isaaclab.utils import configclass

from .flat_env_cfg import SpotFlatEnvCfg

SPOT_ROUGH_TERRAIN_CFG = terrain_gen.TerrainGeneratorCfg(
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
            proportion=0.2, noise_range=(0.02, 0.05), noise_step=0.02, border_width=0.25
        ),
        "stairs_up": terrain_gen.MeshPyramidStairsTerrainCfg(
            proportion=0.25, step_height_range=(0.03, 0.15), step_width=0.3,
            platform_width=3.0, border_width=1.0, holes=False,
        ),
        "stairs_down": terrain_gen.MeshInvertedPyramidStairsTerrainCfg(
            proportion=0.2, step_height_range=(0.03, 0.15), step_width=0.3,
            platform_width=3.0, border_width=1.0, holes=False,
        ),
        "slope_up": terrain_gen.HfPyramidSlopedTerrainCfg(
            proportion=0.15, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
        "slope_down": terrain_gen.HfInvertedPyramidSlopedTerrainCfg(
            proportion=0.1, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
    },
)


@configclass
class SpotRoughEnvCfg(SpotFlatEnvCfg):
    """Same blind observations/actions as the flat task; only the terrain changes."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.terrain.terrain_generator = SPOT_ROUGH_TERRAIN_CFG
        self.scene.terrain.max_init_terrain_level = 2
