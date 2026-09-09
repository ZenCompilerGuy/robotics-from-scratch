# robotics-from-scratch

Control, sensor fusion and probabilistic estimation, built from first principles in Python.
A free, self-paced replacement for the Ubicoders *Robotics 101* course, extended into
probabilistic robotics.

31 lessons, 6 levels, no black boxes. Everything is written from the maths up: the simulators,
the controllers, the filters. No ROS, no library doing the interesting part for you.

## The route

| Level | What gets built |
|---|---|
| **0 — Foundations** | Simulation loops, integrators, rotations and DCMs, PID by feel, noisy sensor models |
| **1 — Control** | A 6-DOF quadcopter from Newton–Euler, flown by a five-loop cascade through a waypoint mission |
| **2 — Sensor fusion** | Complementary and DCM filters recovering attitude from a lying IMU |
| **3 — State space** | `ẋ = Ax + Bu`, pole placement, LQR, an inverted pendulum balanced in NumPy and MuJoCo |
| **4 — Kalman** | The KF derived from multiplying Gaussians, then an EKF hitting <0.5° attitude error |
| **5 — Probabilistic robotics** | Bayes filters, probabilistic motion models, a particle filter solving the kidnapped-robot problem |

## Getting started

Everything installs into a project-local virtual environment — nothing touches your system Python.

**Windows (PowerShell), from the repo root:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

`check_setup.py` refuses to pass unless you're actually inside the venv, so you can't get this
subtly wrong. Every session after the first, just activate — look for the `(.venv)` prefix on
your prompt. Full instructions, VS Code setup and troubleshooting: [`setup/README.md`](setup/README.md).

Then open a Cowork session in the *Learning Probabilistic Robotics* project and say **"Lesson 0.1"**.

## Layout

| Path | What's in it |
|---|---|
| `PLAN.md` | The full framework, curriculum and the reasoning behind both |
| `PROGRESS.md` | Running log — where I am, and each lesson in my own words |
| `PROJECT_INSTRUCTIONS.md` | The tutor brief pasted into the Claude project |
| `setup/` | Virtual environment instructions, requirements, environment checker |
| `srlib/` | The robotics library, built up lesson by lesson |
| `level0/` … `level5/` | Lesson folders: `notes.md`, `lesson.py`, `test_lesson.py`, `sabotage.py` |
| `_solutions/` | Worked solutions, mirrored structure |
| `matlab/` | The four MATLAB/Simulink cross-check scripts |
| `gallery/` | Plots and GIFs — the visible output |

## How each lesson runs

`warm-up → hook → derive the maths → fill in the TODOs → pytest → predict-then-run → break it → log it → commit`

The "break it" step is deliberate: after the tests go green, a sabotaged variant of the working
code gets handed back, and the job is to diagnose it from the plot alone. That's the skill that
separates using robotics code from debugging it.

## Status

**Level 0 — not started.** Plan approved and scaffolding built, 9 September 2026.

## Licence

MIT — see [`LICENSE`](LICENSE). Take anything here and use it however you like.

---

*Adi — MRobotEng, University of Auckland. Mechanical engineer learning robotics properly.*
