# Lesson 0.2 — Discrete time & integration

## Hook: your coffee cup explodes

Newton's law of cooling: `dx/dt = -k(x - x_room)`. Coffee starts at 90°C, room is 20°C, `k`
chosen so it should ease down over a couple of minutes. The simplest update rule that exists:

```
x_new = x + dt * dxdt(x)
```

At `dt = 0.1s` it looks exactly like cooling coffee. Bump `dt` to `1.6s` to make it "run
faster" and by the third or fourth step it reads -1,000-plus degrees, then four figures
positive, flipping sign and growing every step, forever. `k` never changed. Only `dt` did.

## The maths: it's not a blurrier answer, it's a different regime

Let `e = x - x_room`. The ODE becomes `de/dt = -k*e`, with exact solution `e(t) = e0 *
exp(-k*t)` — monotonic decay, same sign as `e0` always, never overshoots.

**Deriving the Euler update.** Euler's whole idea: approximate the derivative by the forward
difference `(e_{n+1} - e_n)/dt ≈ de/dt`, then solve for `e_{n+1}`:

```
(e_{n+1} - e_n)/dt = -k*e_n
e_{n+1} = e_n - k*dt*e_n = (1 - k*dt) * e_n
```

Call `r = 1 - k*dt`. Every step just multiplies by `r`, so after `n` steps: `e_n = r^n * e0`.
The entire behaviour of the simulation is encoded in one number:

- `0 < r < 1` (`k*dt < 1`) — decays to zero, same sign throughout. Coarse but recognisably
  cooling.
- `-1 < r < 0` (`1 < k*dt < 2`) — flips sign every step (overshoots past room temp and back)
  but `|r| < 1` so the overshoot shrinks. Decaying oscillation.
- `r < -1` (`k*dt > 2`) — flips sign AND grows every step. `e0, -1.4e0, 1.96e0, -2.74e0, ...` —
  that's the 90°C → -1000°C → +2000°C sequence.

`dt = 2/k` is a hard threshold, not a gradual accuracy cliff. Crossing it flips whether you're
multiplying by something with magnitude below or above 1, every single step. This is why "just
make dt small enough" is a real constraint on real hardware: a flight controller running at a
fixed loop rate has a `dt` it's stuck with, and a system with fast dynamics (large `k`) can
cross `k*dt > 2` without anyone noticing until it's flying.

**Deriving RK4.** Euler's error all comes from one assumption: the slope at the *start* of the
interval represents the slope for the whole interval. It doesn't — so sample the slope at a few
points inside the interval and average them:

```
k1 = f(t,        x)
k2 = f(t + dt/2, x + dt/2 * k1)     # slope at the midpoint, using k1's estimate of x there
k3 = f(t + dt/2, x + dt/2 * k2)     # slope at the midpoint again, using the better k2 estimate
k4 = f(t + dt,   x + dt   * k3)     # slope at the end, using k3's estimate of x there

x_{n+1} = x_n + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
```

Each `k` uses the previous one to guess where the state will be, then re-evaluates the slope
there. The `1, 2, 2, 1`-over-6 weighting is Simpson's rule for integrating a function from three
sample points (start, mid, end) — the same rule that integrates a curve exactly if it's a cubic
or lower. RK4's local error per step is `O(dt^5)`, global error `O(dt^4)` — versus Euler's
`O(dt)` global error. Halving `dt` barely moves an RK4 result; it visibly improves Euler.

## Assumptions (say them out loud, write them down)

1. **`f` is smooth enough for the Taylor expansion behind all of this to hold.** True for a
   cooling coffee cup or a rigid-body quadcopter; false the instant contact, stiction, or an
   actuator saturation limit enters — exactly why MuJoCo exists later, and why a hand-rolled
   RK4 won't handle it.
2. **Euler evaluates `f` once, at the interval's start, and assumes that slope holds for the
   whole step.** That single assumption is the entire source of its error and its narrow
   stability region.
3. **RK4 assumes 4 samples per step captures the curvature of `f` within that step.** A good
   bet for smooth dynamics; still an imperfect, expensive one near stiff or fast-changing
   regions.
4. **The `2/k` threshold above is exact only because this system is linear** (`de/dt = -k*e`).
   For a nonlinear `f`, Euler is making the same "slope doesn't change over the step"
   assumption locally, but the clean closed-form threshold doesn't carry over directly — Level
   3 covers how to do this analysis (eigenvalues of a linearised system) for anything more
   complex.
5. **RK4 costs 4x the function evaluations per step, Euler costs 1x.** For cheap `f` that's a
   bargain given the accuracy jump. For an expensive `f` (a physics engine, a learned dynamics
   model), that 4x is a real cost to weigh against just shrinking Euler's `dt` instead.

## Resources

- Khan Academy — **Euler's method** (AP Calculus BC, differential equations unit), ~10 minutes.
  Reinforces the geometric-sequence intuition above with a different worked example.
- Wikipedia — **Runge–Kutta methods**, the "The Runge–Kutta method" section. Short read, has the
  `k1..k4` diagram that makes the "sample the slope at intermediate points" idea visual.
