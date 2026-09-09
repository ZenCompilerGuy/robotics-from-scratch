# Euler Integration — Quick Reference

A compact reminder of derivatives, Euler's method, the coffee-cooling example, and the numerical stability condition.

## 1. Core idea: What is a derivative?

A derivative tells you the **current rate of change** of a quantity. For example, if position `x` changes with time `t`, then `dx/dt` is velocity.

```
dx/dt = current slope / current rate of change
```

## 2. What Euler's method does

Euler looks at the current state, calculates the current slope, and assumes that slope stays approximately constant over the next small time interval `dt`.

```
x_new = x + dt · dx/dt
```

More generally:

```
x_{n+1} = x_n + dt · f(x_n)
```

**Mental model**

Look → calculate slope → take a short straight-line step → look again → repeat.

Small `dt`: the straight-line approximation is usually good. Large `dt`: the approximation can become inaccurate, and for some systems it can become unstable.

## 3. Coffee cooling model

Let `x` be coffee temperature and `x_room` be room temperature.

```
dx/dt = −k(x − x_room)
```

Define the temperature error (distance from room temperature):

```
e = x − x_room
de/dt = −k e
```

**What does `k` mean?**

`k` is a property of the physical system. It describes how quickly the error tends to disappear. Larger `k` means faster dynamics. Its units are 1/time (for example, s⁻¹).

## 4. Euler applied to the coffee

Start with Euler:

```
e_new = e + dt · de/dt
```

Since `de/dt = −ke`:

```
e_new = e − k·dt·e
e_new = (1 − k·dt)·e
```

## 5. What is `r`?

`r` is not a physical parameter. It is simply a convenient name for the Euler multiplier:

```
r = 1 − k·dt
```

Therefore: `e_new = r · e`

So `r` tells you exactly what happens to the error in one Euler step: the sign tells you whether it flips sides, and `|r|` tells you whether its magnitude shrinks or grows.

| r | What happens |
|---|---|
| `0 < r < 1` | Error keeps the same sign and shrinks toward zero. |
| `r = 0` | Euler lands exactly at equilibrium in one step. |
| `−1 < r < 0` | Error flips sign, but its magnitude shrinks (decaying oscillation). |
| `r = −1` | Error flips sign with the same magnitude; no decay. |
| `r < −1` | Error flips sign and grows; numerical solution explodes. |

## 6. Euler stability condition

For the error to shrink, we need:

```
|r| < 1
```

Substitute `r = 1 − k·dt`:

```
|1 − k·dt| < 1
0 < k·dt < 2
dt < 2/k
```

This is the Euler stability limit for the simple system `de/dt = −ke`. It is not a universal stability formula for every differential equation.

## 7. Worked coffee example

Suppose room temperature is 20°C, coffee starts at 90°C, and `k = 0.1 s⁻¹`. The initial error is:

```
e_0 = 90 − 20 = 70°C
```

**Case A: dt = 1 s**

```
r = 1 − (0.1)(1) = 0.9
```

Errors: `70 → 63 → 56.7 → 51.03 → …`

Stable: the error shrinks without changing sign.

**Case B: dt = 15 s**

```
r = 1 − (0.1)(15) = −0.5
```

Errors: `70 → −35 → 17.5 → −8.75 → 4.375 → …`

Stable but inaccurate: Euler overshoots room temperature and alternates sides, but the magnitude shrinks because `|r| = 0.5 < 1`.

**Case C: dt = 25 s**

```
r = 1 − (0.1)(25) = −1.5
```

Errors: `70 → −105 → 157.5 → −236.25 → 354.375 → …`

Unstable: the sign flips AND the magnitude grows because `|r| = 1.5 > 1`.

## 8. Accuracy vs. stability

**Accuracy:** How close is the numerical solution to the true physical solution?

**Stability:** Does the numerical solution remain bounded and behave sensibly as the simulation continues?

A larger `dt` can first make Euler less accurate while remaining stable. If `dt` becomes too large, the numerical method can become unstable even when the real physical system is stable.

## 9. The key equations to remember

| Idea | Formula |
|---|---|
| General ODE | `dx/dt = f(x)` |
| Euler update | `x_{n+1} = x_n + dt·f(x_n)` |
| Coffee model | `de/dt = −ke` |
| Euler coffee update | `e_{n+1} = (1 − k·dt)·e_n` |
| Euler multiplier | `r = 1 − k·dt` |
| Repeated steps | `e_n = r^n · e_0` |
| Stability | `\|r\| < 1` |
| Coffee stability limit | `dt < 2/k` |

**One-sentence memory aid:** Euler looks at the current slope and takes a short straight-line step; for the coffee system, `r = 1 − k·dt` determines whether each step shrinks, flips, or explodes the temperature error.
