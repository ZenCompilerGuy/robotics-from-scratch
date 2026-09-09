# Lesson 0.1 — NumPy for robotics

## Hook: your MATLAB muscle memory lies to you here

You've written `x = x + v*dt` a thousand times in MATLAB, where `x` and `v` are vectors. It just
works — elementwise, no fuss. Try the direct Python translation using lists:

```python
x_list = [0.0, 0.0, 0.0]
v_list = [1.0, 2.0, 3.0]
dt = 0.1

result = x_list + v_list * dt
```

This does not raise an error. It does not warn you. It gives you `TypeError: can't multiply
sequence by non-int of type 'float'` on the `v_list * dt` part — and if `dt` were an int, say
`dt = 2`, `v_list * dt` would "succeed" by repeating the list twice (`[1,2,3,1,2,3]`), and
`x_list + (that)` would concatenate rather than add. Nothing crashes. You get a longer list that
looks vaguely plausible if you don't check its length. That is a much worse failure than a
crash — it's the kind that survives into a demo and then into a lab report.

The fix is one word: use `np.array` instead of `list`. Everything below is about *why* that
fixes it, and what rules you're now relying on.

## The maths: what "vectorised" actually means

Forget the word "array" for a second and think about what you want to compute for N particles,
each with a 2D position and a 2D velocity, over one timestep:

```
for i in range(N):
    pos[i] = pos[i] + vel[i] * dt
```

This loop is correct. It is also: slow (Python bytecode overhead per iteration, not the
arithmetic itself), and it scales to more state variables by nesting more loops. Every
"variation on four lines" this course promises you get uglier the moment you loop over indices
by hand.

NumPy's answer is **broadcasting**: define one rule for when two arrays of *different* shapes
are allowed to combine elementwise, and what happens when they do. The rule, compared
right-to-left (trailing dimension first):

1. If the two shapes have the same size in a dimension, that dimension matches as-is.
2. If one of the two has size 1 in a dimension, it is stretched (conceptually repeated) to
   match the other.
3. If a shape has fewer dimensions, it's treated as if it had extra size-1 dimensions on the
   left.
4. If none of the above applies, NumPy refuses — `ValueError: operands could not be broadcast
   together` — loudly, at the point of the mistake. Compare that to the list version's silent
   wrong answer. A loud failure is a gift.

For `pos` shaped `(N, 2)` and `vel` shaped `(N, 2)`: same shape, rule 1 applies in both
dimensions, done — this is just elementwise addition, no stretching needed. `pos + vel * dt`
is the whole update, no loop.

Where it gets interesting — and where today's sabotage lives — is when the shapes *aren't*
equal but still "broadcast". `(N, 2)` combined with `(2,)` is legal: rule 3 treats `(2,)` as
`(1, 2)`, then rule 2 stretches the size-1 dimension to `N`, so a *single* 2D vector gets
applied to *every* row. That's exactly what you want when adding a constant like gravity to
every particle. It's exactly what you *don't* want if `(2,)` was supposed to be "particle 0's
velocity" and got there by an indexing mistake — every particle silently inherits particle 0's
motion, and NumPy will not complain, because as far as the broadcasting rule is concerned,
nothing is wrong.

## Assumptions (say them out loud, write them down)

1. **Every element in an array shares one dtype.** Unlike a Python list, you can't casually mix
   an `int` index and a `float` measurement in the same array — NumPy silently upcasts to a
   common type. Usually harmless, but it's why comparing floats for exact equality later in
   this course will bite you, and why `test_lesson.py` uses `np.testing.assert_allclose`
   instead of `==`.
2. **Broadcasting compares shapes right-to-left; "1" is the only wildcard.** There is no rule
   that says "and also broadcast if the sizes are just kind of close." Two mismatched non-1
   dimensions are always an error.
3. **Slicing gives you a *view*, not a copy** (`vel[0]` shares memory with `vel`). Today's
   `update_positions` is written as a pure function — it returns a brand-new array rather than
   mutating its input — so `.copy()` isn't strictly load-bearing yet inside `run_particles`.
   Keep writing it anyway (`log.record(pos=pos.copy())`). The moment any part of this course
   switches to an in-place update for speed — and some will, once performance starts to matter
   — skipping `.copy()` turns "record history" into "record N references to the same array,"
   and your entire logged trajectory silently collapses to whatever the final value turned out
   to be. That bug is miserable to find after the fact; it's free to prevent now.

## Resource

- NumPy's own **Broadcasting** page: <https://numpy.org/doc/stable/user/basics.broadcasting.html>
  — ~10 minutes, official, and it's the primary source for the rule above (read it if my
  version left anything unclear).
