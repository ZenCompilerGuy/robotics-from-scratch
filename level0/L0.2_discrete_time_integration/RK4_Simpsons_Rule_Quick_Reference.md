# RK4 & Simpson's Rule — Quick Reference

A compact study sheet connecting Euler's approximation, Runge–Kutta 4th order (RK4), and Simpson's numerical integration rule.

## 1. Why does the slope change?

For an ODE, the derivative is generally a function of the current time and state:

```
dx/dt = f(t, x)
```

As `x` changes, `f(t,x)` can change. Therefore the slope can change even in a perfectly controlled environment. Environmental disturbances are only one possible additional cause.

Coffee: `de/dt = −ke`. When the temperature error `e` is large, the cooling rate is large. As `e` approaches zero, the cooling rate approaches zero.

## 2. Euler's method

Euler evaluates the slope once, at the beginning of the timestep, and assumes that slope is approximately valid throughout the step.

```
x_{n+1} = x_n + dt · f(t_n, x_n)
```

**Mental model:** Look at the current slope → assume it stays constant briefly → move → recalculate.

## 3. RK4: the central idea

RK4 samples the slope four times within one timestep. Later slope estimates use earlier estimates to predict where the state will be.

| Stage | Formula | Meaning |
|---|---|---|
| `k1` | `f(t_n, x_n)` | Slope at start |
| `k2` | `f(t_n + dt/2, x_n + (dt/2)·k1)` | Midpoint using `k1` |
| `k3` | `f(t_n + dt/2, x_n + (dt/2)·k2)` | Improved midpoint |
| `k4` | `f(t_n + dt, x_n + dt·k3)` | Slope at end |

```
x_{n+1} = x_n + (dt/6)·(k1 + 2k2 + 2k3 + k4)
```

**Memory aid:** Start → midpoint → midpoint again → end → weighted combination.

## 4. Why four stages?

`k1`: What is the slope now?
`k2`: If I follow `k1` halfway, what is the slope there?
`k3`: Using the better midpoint estimate, what is the slope there?
`k4`: Using `k3`, what is the slope at the end?
**Final:** Combine them to estimate the average slope over the interval.

## 5. Simpson's rule

Simpson's rule estimates the area under a curve (a definite integral) using values at the start, midpoint, and end. It gives greater weight to the interior point.

```
∫[a to b] f(x) dx ≈ (b−a)/6 · [f(a) + 4f((a+b)/2) + f(b)]
```

Weighting: `1 : 4 : 1`. For composite Simpson's rule the pattern becomes `1, 4, 2, 4, 2, …, 4, 1`.

## 6. Simpson's rule and RK4

RK4 uses the related weighting pattern `1 : 2 : 2 : 1`. The resemblance is useful intuition, but RK4 is **not simply Simpson's rule applied to `f`**. Its `k2`, `k3`, and `k4` values are evaluated at predicted states.

## 7. Small comparison

For `dx/dt = x`, starting from `x = 1` with `dt = 0.1`:

| Method | After one step | Comment |
|---|---|---|
| Exact | 1.1051709 | Ground truth: `e^0.1` |
| Euler | 1.1000000 | Uses only the starting slope |
| RK4 | 1.1051708 | Very close to exact |

## 8. Euler vs RK4

| Feature | Euler | RK4 |
|---|---|---|
| Slope evaluations / step | 1 | 4 |
| Looks inside step? | No | Yes |
| Global error | `O(dt)` | `O(dt^4)` |
| Cost / step | Low | ≈4× function evaluations |
| Main idea | Starting slope | Several predicted slopes |

## 9. What does 4th order mean?

For smooth problems, Euler's global error scales roughly as `dt`, while RK4's global error scales roughly as `dt^4`.

```
Halve dt → Euler error ≈ 1/2 as large.
Halve dt → RK4 error ≈ 1/16 as large.
```

These are asymptotic accuracy statements: they assume sufficiently small `dt` and sufficiently smooth dynamics.

## 10. Final memory map

**Euler:** One slope → one straight-line prediction.
**RK4:** Four intelligently predicted slopes → weighted average slope → one update.
**Simpson:** Start/middle/end values → weighted estimate of area under a curve.

**Key idea:** The slope changes because `f` depends on the changing state (and possibly time), not necessarily because the environment is irregular.
