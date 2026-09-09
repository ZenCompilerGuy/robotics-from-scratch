# euler_step, rk4_step and simulate as they should end up inside srlib/sim.py
# after L0.2. Paste these in to replace the three NotImplementedError bodies
# (Logger is already filled in from L0.1 -- leave it as is).

def euler_step(f, t, x, u, dt):
    k1 = f(t, x, u)
    return x + dt * k1


def rk4_step(f, t, x, u, dt):
    k1 = f(t, x, u)
    k2 = f(t + dt / 2, x + dt / 2 * k1, u)
    k3 = f(t + dt / 2, x + dt / 2 * k2, u)
    k4 = f(t + dt, x + dt * k3, u)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(f, x0, controller, t_end, dt, integrator=rk4_step):
    log = Logger()
    x = x0.copy()
    t = 0.0
    while t < t_end:
        u = controller(t, x)
        log.record(t=t, x=x.copy(), u=u.copy() if hasattr(u, "copy") else u)
        x = integrator(f, t, x, u, dt)
        t += dt
    return log.as_dict()
