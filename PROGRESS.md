# Progress log

Where I am, and what I've actually understood. Three sentences per lesson, in my own words — no copied jargon.

**Current position:** Level 0, Lesson 0.2 complete
**Last session:** 9 September 2026

---

## Level 0 — Foundations

| Lesson | Done | Tests green | Boss fight |
|---|---|---|---|
| 0.1 NumPy for robotics | ☑ | ☑ | |
| 0.2 Discrete time & integration | ☑ | ☑ | |
| 0.3 Live plotting & logging | ☐ | ☐ | |
| 0.4 Trig, Taylor, small-angle | ☐ | ☐ | |
| 0.5 Linear algebra that matters | ☐ | ☐ | |
| 0.6 Rotations I — 2D & frames | ☐ | ☐ | |
| 0.7 Rotations II — 3D, DCM, Euler | ☐ | ☐ | |
| 0.8 PID by feel | ☐ | ☐ | |
| 0.9 Sensors lie | ☐ | ☐ | |
| **BF0 — 1D drone altitude hold** | | | ☐ |

*(Levels 1–5 tables added as we reach them.)*

---

## Notes to self

*(Your three sentences per lesson go here. Also: anything that didn't click, so we can come back to it.)*

### L0.1 -- NumPy for robotics

1. Python treats a plain list as a collection of objects, not a mathematical vector -- operators like `+` and `*` don't act elementwise on it. A NumPy array behaves like a single mathematical object, so a scalar or another array broadcasts across every element automatically, without writing a for loop. That's vectorisation.
2. `np.linalg.norm` isn't a mean of anything -- it's the square root of the sum of the squared components. Used on `(vx, vy)`, that's exactly the vector's magnitude, i.e. speed.
3. Speed is how fast the particle is moving, with direction stripped out -- that's what makes it a scalar instead of a vector (velocity).
4. Dictionaries are a good way to store multiple named signals like position and velocity, since each name maps to its own growing list of values.
5. `**kwargs` collects any number of keyword arguments into a dictionary inside the function, which is how `Logger.record` can accept an arbitrary set of named signals.

### L0.2 -- Discrete time & integration

1. Euler assumes that the data point in the next time step follows the same slope as the previous point was following -- it only ever looks at the slope once, at the start of the interval.
2. RK4 doesn't assume a single slope value -- it takes around four slope values, each one built by taking the previous slope estimate into reference: one at the start, two at the midpoint of the interval, and one at the end, and (Simpson's-rule style) the midpoint slopes are given more weightage in the final summation, which is why the whole thing is divided by 6.
3. The RK4 value came out much closer to the analytical solution than Euler's, even under stable conditions -- not only when Euler is about to blow up.
4. `r` (`= 1 - k*dt`) is not actually a physical parameter, it's just a convenient way to represent the Euler multiplier -- it tells you exactly what happens to the error in one Euler step: whether the magnitude increases, decreases, or whether it flips sides.

Sabotage: the "RK4" was fake -- it evaluated all four k's at the same point instead of using the previous slope estimates to predict the midpoint and end states, so it collapsed to plain Euler and diverged at the same dt.

---

## Questions I still have

*(Park anything unresolved here rather than letting it slide.)*
