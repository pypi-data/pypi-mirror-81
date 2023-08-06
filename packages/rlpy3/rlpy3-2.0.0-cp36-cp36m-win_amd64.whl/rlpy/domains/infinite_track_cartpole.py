"""Pendulum base domain."""
import numpy as np
from .cartpole_base import CartPoleBase, StateIndex

__copyright__ = "Copyright 2013, RLPy http://acl.mit.edu/RLPy"
__credits__ = [
    "Alborz Geramifard",
    "Robert H. Klein",
    "Christoph Dann",
    "William Dabney",
    "Jonathan P. How",
]
__license__ = "BSD 3-Clause"
__author__ = ["Robert H. Klein"]


class InfTrackCartPole(CartPoleBase):

    """
    Infinite Track Cart Pole.

    Inherits dynamics from ``CartPoleBase`` and utilizes two states - the
    angular position and velocity of the pendulum on the cart.
    This domain is effectively a CartPole moving on an infinite rail.

    An identical physical implementation consists of a pendulum mounted instead
    on a rotating rod. (if the length of the rod to pendulum base is assumed
    to be 1.0m, then force actions on the cart (Newtons) correspond directly
    to torques on the rod (N*m).)

    See `Tor Aamodt's B.A.Sc. Thesis <http://www.eecg.utoronto.ca/~aamodt/BAScThesis/>`_
    for a visualization.

    .. warning::
        In the literature, this domain is often referred as a ``Pendulum`` and
        is often accompanied by misleading or even incorrect diagrams.
        However, the cited underlying dynamics correspond to a pendulum on a
        cart (:class:`domains.CartPoleBase.CartPoleBase`), with
        cart position and velocity ignored and unbounded
        (but **still impacting the pendulum dynamics**).

        Actions thus still take the form of forces and not torques.

    **State**

    theta    = Angular position of pendulum (relative to straight up at 0 rad), positive clockwise.
    thetaDot = Angular rate of pendulum. positive clockwise.

    **Actions**

    Actions take the form of force applied to cart;
    Positive force acts to the right on the cart.

    Uniformly distributed noise is added with magnitude 10 N.

    .. seealso::
        Michail G. Lagoudakis, Ronald Parr, and L. Bartlett
        Least-squares policy iteration.  Journal of Machine Learning Research
        (2003) Issue 4.

    .. note::
        for full domain description, see:
        Wang, H., Tanaka, K., and Griffin, M. An approach to fuzzy control
        of nonlinear systems; Stability and design issues.
        IEEE Trans. on Fuzzy Systems, 4(1):14-23, 1996.

    .. note::
        See also `RL-Library CartPole <http://library.rl-community.org/wiki/CartPole>`_
        Domain constants per RL Community / RL_Glue
        `CartPole implementation <http://code.google.com/p/rl-library/wiki/CartpoleJava>`_

    """

    __author__ = "Robert H. Klein"

    #: Default limits on theta
    ANGLE_LIMITS = [-np.pi / 15, np.pi / 15]
    #: Default limits on pendulum rate
    ANGULAR_RATE_LIMITS = [-2.0, 2.0]
    #: m - Default limits on cart position (this state is ignored by the agent)
    POSITION_LIMITS = [-np.inf, np.inf]
    #: m/s - Default limits on cart velocity (this state is ignored by the agent)
    VELOCITY_LIMITS = [-np.inf, np.inf]

    # Newtons, N - Torque values available as actions
    AVAIL_FORCE = np.array([-50, 0, 50])

    # kilograms, kg - Mass of the pendulum arm
    MASS_PEND = 2.0
    # kilograms, kg - Mass of cart
    MASS_CART = 8.0
    # meters, m - Physical length of the pendulum, meters (note the moment-arm
    # lies at half this distance)
    LENGTH = 1.0
    # m - Length of moment-arm to center of mass (= half the pendulum length)
    MOMENT_ARM = LENGTH / 2
    # 1/kg - Used in dynamics computations, equal to 1 / (MASS_PEND +
    # MASS_CART)
    _ALPHA_MASS = 1 / (MASS_CART + MASS_PEND)
    # Time between steps
    dt = 0.1
    # Newtons, N - Maximum noise possible, uniformly distributed
    force_noise_max = 10

    int_type = "rk4"

    def __init__(self, **kwargs):
        self.dim_names = ["Theta", "Thetadot"]
        super().__init__(
            statespace_limits=np.array([self.ANGLE_LIMITS, self.ANGULAR_RATE_LIMITS]),
            continuous_dims=[StateIndex.THETA, StateIndex.THETA_DOT],
            **kwargs
        )

    def s0(self):
        # Defined by children
        raise NotImplementedError

    def step(self, a):
        """
        Append arbitrary lateral position and velocity of cart: ``[0,0]``
        and perform a ``step()``.
        """
        # import ipdb; ipdb.set_trace()
        s = np.append(self.state, np.array([0, 0]))  # 0 cart position and velocity
        ns = self._stepFourState(s, a)
        ns = ns[0:2]  # [theta,thetadot], ie, omitting position/velocity of cart
        self.state = ns.copy()

        terminal = self.is_terminal()  # automatically uses self.state
        reward = self._getReward(a)  # Automatically uses self.state
        possible_actions = self.possible_actions()
        return reward, ns, terminal, possible_actions

    def show_domain(self, a=0):
        """
        Display the 4-d state of the cartpole and arrow indicating current
        force action (not including noise!).
        Note that for 2-D systems the cartpole is still displayed, but appears
        static; see :class:`domains.infinite_track_cartpole.InfTrackCartPole`.

        """
        # 0 cart position and velocity
        fourState = np.append(self.state, np.array([0, 0]))
        self._plot_state(fourState, a)

    def show_learning(self, representation):
        thetas, theta_dots = self._setup_learning(representation)
        pi = np.zeros((len(theta_dots), len(thetas)), np.uint8)
        V = np.zeros((len(theta_dots), len(thetas)))

        for row, thetaDot in enumerate(theta_dots):
            for col, theta in enumerate(thetas):
                s = np.array([theta, thetaDot])
                terminal = self.is_terminal(s)
                # Array of Q-function evaluated at all possible actions at
                # state s
                Qs = representation.Qs(s, terminal)
                # Array of all possible actions at state s
                As = self.possible_actions(s=s)

                # If multiple optimal actions, pick one randomly
                a = np.random.choice(As[Qs.max() == Qs])
                # Assign pi to be an optimal action (which maximizes
                # Q-function)
                pi[row, col] = a
                # Assign V to be the value of the Q-function under optimal
                # action
                V[row, col] = max(Qs)

        self._plot_policy(pi)
        self._plot_valfun(V)
        self.policy_fig.canvas.draw()
        self.value_fn_fig.canvas.draw()


class InfCartPoleBalance(InfTrackCartPole):

    """
    **Goal**: \n
    Balance the Pendulum on the cart, not letting it fall below horizontal.

    **Reward**: \n
    Penalty of ``FELL_REWARD`` is received when pendulum falls below horizontal,
    zero otherwise.
    \n
    Domain constants per 1Link implementation by Lagoudakis & Parr, 2003.

    .. warning::

        L+P's rate limits [-2,2] are actually unphysically slow, and the pendulum
        saturates them frequently when falling; more realistic to use 2*pi.

    """

    __author__ = "Robert H. Klein"

    #: Reward received when the pendulum falls below the horizontal
    FELL_REWARD = -1
    #: Limit on theta (Note that this may affect your representation's discretization)
    ANGLE_LIMITS = [-np.pi / 2, np.pi / 2]
    #: Limits on pendulum rate, per 1Link of Lagoudakis & Parr
    ANGULAR_RATE_LIMITS = [-2.0, 2.0]
    # NOTE that L+P's rate limits [-2,2] are actually unphysically slow, and the pendulum
    # saturates them frequently when falling; more
    # realistic to use 2*pi.

    def __init__(self, episode_cap=3000):
        super().__init__(episode_cap=episode_cap)

    def s0(self):
        # import ipdb; ipdb.set_trace()
        # Returns the initial state, pendulum vertical
        # Initial state is uniformly random between [-.2,.2] for both
        # dimensions
        self.state = (self.random_state.rand(2) * 2 - 1) * 0.2
        return self.state.copy(), self.is_terminal(), self.possible_actions()

    def _getReward(self, a, s=None):
        # Return the reward earned for this state-action pair
        # On this domain, reward of -1 is given for failure, |angle| exceeding
        # pi/2
        if s is None:
            s = self.state
        return self.FELL_REWARD if self.is_terminal(s=s) else 0

    def is_terminal(self, s=None):
        if s is None:
            s = self.state
        return not -np.pi / 2.0 < s[StateIndex.THETA] < np.pi / 2.0


class InfCartPoleSwingUp(InfTrackCartPole):

    """
    **Goal** \n
    Reward is 1 whenever ``theta`` is within ``GOAL_LIMITS``, 0 elsewhere.\n
    There is no terminal condition aside from ``episode_cap``.\n

    Pendulum starts straight down, ``theta = pi``.  The task is to swing it up,
    after which the problem reduces to
    :class:`domains.infinite_track_cartpole.InfCartPoleBalance`, though
    with (possibly) different domain constants defined below.

    """

    __author__ = "Robert H. Klein"

    #: Goal region for reward
    GOAL_LIMITS = [-np.pi / 6, np.pi / 6]
    #: Limits on theta
    ANGLE_LIMITS = [-np.pi, np.pi]
    #: Limits on pendulum rate
    ANGULAR_RATE_LIMITS = [-3 * np.pi, 3 * np.pi]

    def __init__(self):
        super().__init__(discount_factor=0.9, episode_cap=300)

    def s0(self):
        """ Returns the initial state: pendulum straight up and unmoving. """
        self.state = np.array([np.pi, 0])
        return self.state.copy(), self.is_terminal(), self.possible_actions()

    def _getReward(self, a, s=None):
        """
        Return the reward earned for this state-action pair.
        On this domain, reward of 1 is given for success, which occurs when
        |theta| < pi/6
        """
        if s is None:
            s = self.state
        return (
            self.GOAL_REWARD
            if self.GOAL_LIMITS[0] < s[StateIndex.THETA] < self.GOAL_LIMITS[1]
            else 0
        )

    def is_terminal(self, s=None):
        return False
