"""
srlib.robots — the plants. The things you're trying to control.

    quad.py       6-DOF quadcopter          L1.1, flown through L1.5
    cartpole.py   inverted pendulum on cart L3.5, ported to MuJoCo in BF3
    diffdrive.py  differential-drive UGV    L5.x, the capstone robot

Every one of them is a `dynamics(t, x, u) -> xdot` function wrapped in a class
that knows its own parameters. Nothing is a black box — when your drone flips,
you can open the file and find the sign error you wrote.
"""
