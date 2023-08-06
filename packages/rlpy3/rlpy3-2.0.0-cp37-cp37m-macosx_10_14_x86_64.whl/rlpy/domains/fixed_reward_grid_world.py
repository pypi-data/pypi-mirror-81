"""FixedRewardGridworld Domain."""
import itertools
import numpy as np
from rlpy.tools import __rlpy_location__, plt, with_bold_fonts
from pathlib import Path

from .grid_world import GridWorld

__license__ = "BSD 3-Clause"
__author__ = "Yuji Kanagawa"


class FixedRewardGridWorld(GridWorld):
    """The same as GridWorld, but you can set any reward for each cell.
    """

    # directory of maps shipped with rlpy
    DEFAULT_MAP_DIR = Path(__rlpy_location__).joinpath(
        "domains/FixedRewardGridWorldMaps"
    )

    def _load_map(self, mapfile):
        map_and_reward = np.loadtxt(mapfile, dtype=np.float64)
        mshape = map_and_reward.shape
        if mshape[0] % 2 == 1:
            raise ValueError("Invalid map with shape {}".format(mshape))
        col = mshape[0] // 2
        self.reward_map = map_and_reward[col:]
        return map_and_reward[:col].astype(np.int32)

    def __init__(
        self,
        mapfile=DEFAULT_MAP_DIR.joinpath("6x6guided.txt"),
        noise=0.1,
        random_start=False,
        random_goal=False,
        episode_cap=lambda height, width: (width + height) * 2,
        step_penalty=None,
    ):
        super().__init__(
            mapfile=mapfile,
            noise=noise,
            random_start=random_start,
            random_goal=random_goal,
            episode_cap=episode_cap,
        )
        if step_penalty is None:
            step_penalty = self.reward_map.max() / 1000
        self.step_penalty = step_penalty

    def _reward(self, next_state, terminal):
        reward = self.reward_map[next_state[0], next_state[1]]
        if not terminal:
            reward -= self.step_penalty
        return reward

    def _rew_range(self):
        mi, ma = 1000, -1000
        for r, c in itertools.product(range(self.rows), range(self.cols)):
            if self.map[r, c] == self.EMPTY:
                mi = min(mi, self.reward_map[r, c])
                ma = max(ma, self.reward_map[r, c])
        if mi == 1000:
            mi = min(self.reward_map[r, c])
        if ma == -1000:
            ma = max(self.reward_map[r, c])
        return mi, ma

    def _show_numbers(self):
        cmap = plt.get_cmap("ValueFunction-New")
        rw_min, rw_max = self._rew_range()
        for r, c in itertools.product(range(self.rows), range(self.cols)):
            if self.reward_map[r, c] == 0:
                continue
            raw_reward = self.reward_map[r, c]
            if self.map[r, c] == self.EMPTY:
                if rw_max > rw_min:
                    reward = (self.reward_map[r, c] - rw_min) / (rw_max - rw_min)
                else:
                    reward = 0.7
                color = cmap(reward)
            elif self.map[r, c] in [self.GOAL, self.PIT]:
                color = "w"
            else:
                continue
            self.domain_ax.text(
                c - 0.4, r + 0.1, str(raw_reward), color=color, fontsize=12.0,
            )

    def _show_map(self, legend=False):
        super()._show_map(legend=legend)
        with with_bold_fonts():
            self._show_numbers()
