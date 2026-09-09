# Robotics from Scratch — Framework & Implementation Plan

**For:** Adi — MRobotEng, University of Auckland
**Built as a free, self-paced replacement for:** Ubicoders *Robotics 101 — Control & Estimation for a UAV or UGV, built from scratch* (68 lessons, 8 modules)
**Status:** Approved. Scaffolding built, repo initialised. Next action is Lesson 0.1, in a new conversation.
**Date:** drafted 8 September 2026, approved and updated 9 September 2026

---

## 0. Three honest things before you read the plan

**1. "Stochastic robotics" is not really the name of the field.** The standard academic name is **probabilistic robotics** — Thrun, Burgard and Fox's term, and the title of the field's standard textbook. If you search "stochastic robotics" you'll find a scattering of papers using it loosely. Search "probabilistic robotics" and you'll find the actual body of work: Bayes filters, Kalman filters, particle filters, SLAM, POMDPs. Use the right word in your Master's and people will know what you mean. I'll use *probabilistic* from here on.

**2. The course you found is not a stochastic robotics course.** It is a **control and estimation** course. Roughly 70% control (PID, cascaded loops, state space, LQR) and 30% estimation (complementary filter, DCM fusion, Kalman/EKF). Only the last four lessons are genuinely probabilistic. This is not a criticism of the course — it's a good curriculum, and its content is exactly the foundation you need. But if your goal is probabilistic robotics, the course is the *runway*, not the destination. So this plan covers all of it and then adds a proper probabilistic capstone (Level 5).

**3. Your instinct about the three pillars is right, with one addition.** You said sensor fusion, control systems, decision making. That's a good decomposition. The thing sitting underneath all three, and the thing that makes them one subject rather than three, is **state estimation under uncertainty** — the idea that a robot never knows where it is, only a probability distribution over where it might be, and that control and decision-making are both operations on that distribution. Every level below is built to make that one idea land physically, not just algebraically.

---

## 1. What you'll be able to do at the end

Concrete, testable, and matched to what the course page advertises:

- Write a quadcopter simulator from Newton–Euler equations, and fly it through a waypoint mission with a five-loop cascaded controller you wrote yourself.
- Take a stream of noisy, biased, drifting IMU data and recover the attitude to under a degree, using a DCM complementary filter *and* an EKF — and explain in one sentence why each works.
- Write `ẋ = Ax + Bu` for a mechanical system, linearise it, check its stability from the eigenvalues, and design pole-placement and LQR controllers to balance an inverted pendulum.
- Derive the Kalman filter from "multiplying two Gaussians" rather than memorising five matrix equations, then implement it in about ten lines.
- Build a particle filter that localises a wheeled robot in a known map from a noisy range sensor — the "kidnapped robot" problem.
- Read a robotics paper's methods section and recognise what the symbols are doing.

**Portfolio output:** one clean public GitHub repo with six runnable simulations and animated GIFs. This is worth more to you than a certificate, and you'll have it either way.

---

## 2. Design of the framework

### 2.1 The loop that every lesson runs

The course calls its method the MCP loop: Math → Code → connect with Physical robots. I'm keeping it and adding two steps that are where learning actually happens:

| Step | What happens | Why it's there |
|---|---|---|
| **0. Warm-up** | I ask you 3 fast retrieval questions from earlier lessons. No looking back. | Spaced retrieval. This is the single highest-yield study technique there is, and it costs 90 seconds. |
| **1. Hook** | I show you something that *fails*, or a physical phenomenon with no explanation yet. | You can't appreciate an answer until you've felt the question. |
| **2. Maths** | We derive the equation. Every assumption gets said out loud and written down. | Assumptions are where robotics breaks in the real world. Memorised formulas are useless; known-assumption formulas are engineering. |
| **3. Code** | You get a file with working scaffolding and the 10 important lines blanked out as `TODO`. Plus a test file. | You write only the part that carries the idea. Everything boring is done for you. |
| **4. Predict → Run** | Before you run it, you write down what the plot will look like. Then run. | Prediction-then-feedback beats passive observation by a wide margin. A wrong prediction is the most valuable event in the lesson. |
| **5. Break it** | I hand you a sabotage: a sign flipped, a gain doubled, a `dt` made too big, noise turned up. You diagnose it from the plot alone. | This is the skill that separates people who *use* robotics code from people who *debug* it. It is also, unglamorously, most of the job. |
| **6. Log** | You write 3 sentences in `PROGRESS.md`, in your own words, no jargon copied from me. | If you can't say it plainly you don't have it yet. This file also becomes your revision notes for the Master's. |

### 2.2 How you know you've actually got it (no waiting on me)

Every lesson ships with a **pytest file**. Run `pytest` — green means your maths is right, red tells you which property failed. You are never stuck waiting for me to mark something. Tests check real properties, not string matches:

- a rotation matrix must satisfy `R @ R.T == I` and `det(R) == 1`
- a Kalman filter's covariance must decrease when a measurement arrives
- a closed-loop A-matrix's eigenvalues must be where you placed them
- a controller must settle within a tolerance band in under N seconds

Solutions live in a `_solutions/` folder. They're there from day one, unlocked — I'm not going to treat you like a child about it. Use them when you're properly stuck after a genuine attempt; you'll know when you're cheating yourself.

### 2.3 Boss fights

Each level ends with an integrated challenge with **no scaffolding** — a blank file, a spec, and a test file. This is the honest check that you can assemble the pieces, not just fill in blanks. If you can't do a boss fight, that level isn't finished, and we go back. That's the only gate in the whole plan.

### 2.4 Two simulators, on purpose

You chose both, which is the right call:

- **Hand-built NumPy sims** for Levels 0–4. Every equation is visible and editable. When your drone flips, you can trace it to a line of physics *you wrote*. This is where the maths intuition is built.
- **MuJoCo** for the Level 3 pendulum port and the Level 5 capstone. Free, real contact dynamics, a proper 3D view, and it's what a lot of real research code uses. Once your controller works in your own sim, porting it to MuJoCo and watching it *still work* is the moment the subject stops feeling like homework.

### 2.5 MATLAB / Simulink's role

Python is primary. MATLAB appears in exactly four places, as a cross-check, because seeing the same idea in two notations is what makes it stick and because your department will use it:

- **L3.1** — build the mass-spring-damper in Simulink as a block diagram, next to your NumPy version. The block diagram *is* the differential equation; seeing that once is worth an hour of algebra.
- **L3.3–3.4** — `place()` and `lqr()` from Control System Toolbox, checked against your hand-written implementations. If your gains match MATLAB's, you implemented it correctly.
- **L3.x** — root locus and Bode plots. Easier to explore interactively in MATLAB than to build from scratch.
- **L4.3** — `kalman()` as a sanity check on your filter.

Everything else is Python. If your student MATLAB licence ends, nothing in this course dies with it.

---

## 3. Curriculum

**~31 lessons across 6 levels.** Each lesson is roughly one sitting: 90 minutes to 3 hours depending on how deep you go on the "break it" step. No dates, no deadlines. You come back when you come back; the folder remembers where you were.

Mapping to the original course is shown so you can see nothing is missing.

---

### **Level 0 — Foundations: the toolkit and the first controller**
*Covers course Modules 02 and 03 (32 lessons there → 9 here, because you already have engineering maths)*

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 0.1 | NumPy for robotics | Arrays are vectors and matrices, not lists. Broadcasting. Why loops are the enemy. | A simulation loop skeleton you'll reuse 30 times |
| 0.2 | Discrete time & integration | Real robots don't have `dt → 0`. Euler vs RK4, and what "unstable because your timestep is too big" looks like on a plot | Two integrators, side by side, diverging |
| 0.3 | Live plotting & data logging | You cannot debug what you cannot see | A reusable real-time dashboard (`srlib/plotting.py`) |
| 0.4 | Trig, Taylor, small-angle | Linearisation is just "throw away the terms that don't matter near here" — the single most-used trick in the field | A plot of where `sin θ ≈ θ` stops being a lie |
| 0.5 | Linear algebra that matters | A matrix is a *transformation*. Eigenvectors are the directions it doesn't rotate. Eigenvalues are stability. | Vector-field visualiser |
| 0.6 | Rotations I — 2D & frames | "Body frame vs world frame" is 80% of robotics bugs | 2D rotation, frame-transform exercises |
| 0.7 | Rotations II — 3D, DCM, Euler | Rotations don't commute; gimbal lock is real; Rodrigues integrates angular rate into a DCM | `srlib/rotations.py` — your own rotation library |
| 0.8 | P, PI, PD, PID by feel | P wobbles, D brakes, I kills steady-state bias. Tuned by intuition first, theory later | A PID class, and a mass you can shove |
| 0.9 | Sensors lie | Noise, bias, drift, quantisation, latency. Moving-average and first-order low-pass filters, and the lag you pay for smoothness | `srlib/sensors.py` — a realistic fake IMU |
| **BF0** | **Boss fight** | — | **1D drone: hold altitude with a noisy altimeter and a PID. Blank file.** |

---

### **Level 1 — Control: making a quadcopter fly**
*Covers course Module 04*

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 1.1 | Quadcopter dynamics | Four thrusts become one force and three torques. The motor mixer is a 4×4 matrix. | `srlib/robots/quad.py` — 6-DOF simulator |
| 1.2 | Rate loop (innermost) | The fastest loop controls angular velocity. Everything else sits on top of it. | Rate PID; step-response plots |
| 1.3 | Attitude loop | Attitude control *commands* rate control. Cascade = each loop sees a plant that's already stabilised | Attitude PID over the rate loop |
| 1.4 | Velocity & position loops | Five nested loops: position → velocity → attitude → rate → mixer. Why the inner loop must be ~5× faster | Full cascade |
| 1.5 | Missions | Waypoints, tolerance radii, state machines, return-to-home | Mission executor |
| **BF1** | **Boss fight** | — | **Take off, fly a 4-waypoint square, return home, land. Wind disturbance on.** |

---

### **Level 2 — Sensor fusion: two liars make one honest answer**
*Covers course Module 05*

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 2.1 | Complementary filter | Gyro is right in the short term and drifts; accelerometer is right on average and is noisy. Trust each where it's good — a high-pass and a low-pass that sum to one | 1-axis complementary filter |
| 2.2 | Attitude from accel + mag | Gravity gives you roll and pitch; the magnetic field gives you yaw. And why this fails the moment the robot accelerates | Static attitude estimator |
| 2.3 | DCM fusion | Gyro *predicts* the DCM; accel/mag *correct* it. The error is a cross product; the correction is a PI controller; orthonormalisation stops numerical drift | Full DCM fusion |
| **BF2** | **Boss fight** | — | **Attitude from a noisy, biased, drifting IMU on a manoeuvring drone. Ground truth hidden until you submit.** |

---

### **Level 3 — State space: the language robotics is actually written in**
*Covers course Module 06. MATLAB/Simulink appears here.*

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 3.1 | `ẋ = Ax + Bu` | Any linear system, any order, one equation. The vector field *is* the system | Mass-spring-damper: NumPy + Simulink, side by side |
| 3.2 | Stability from eigenvalues | Eigenvalues in the left half-plane = stable. That's it. That's the rule | Pole-location → response-shape atlas |
| 3.3 | Pole placement | If you can steer the system's own eigenvalues, you can choose how it behaves. Controllability is the catch | `place()`, hand-written, checked against MATLAB |
| 3.4 | LQR | Stop guessing poles. Write down what you *care about* (Q and R), and the optimal gain falls out | LQR solver; Q/R tuning experiments |
| 3.5 | Inverted pendulum | Linearise about the unstable equilibrium; balance it. The classic, for good reason | Cart-pole in NumPy |
| **BF3** | **Boss fight** | — | **Balance a cart-pole with LQR from a blank file, then port it to MuJoCo and watch it survive real contact physics. Stretch: energy-based swing-up.** |

---

### **Level 4 — The Kalman filter: estimation done properly**
*Covers course Module 07*

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 4.1 | Gaussians & covariance | A belief is a distribution. Multiplying two Gaussians gives a *tighter* Gaussian — that is the entire Kalman filter in one sentence | Gaussian multiplication visualiser |
| 4.2 | The 1D Kalman filter | Predict widens the belief, update narrows it. Ten lines. No matrices yet | Scalar KF tracking a noisy value |
| 4.3 | The multivariate KF | What F, Q, H, R, P and K each physically mean. Why K is a *trust ratio* | 2D position+velocity tracker |
| 4.4 | The EKF | Reality is non-linear. Linearise at the current estimate using a Jacobian, every step. And where it fails | EKF for Euler-angle estimation, target <0.5° |
| **BF4** | **Boss fight** | — | **EKF attitude estimation on the Level 2 dataset. Beat your complementary filter's RMS error.** |

---

### **Level 5 — Probabilistic robotics: the actual field you named**
*Beyond the original course. This is the payoff.*

**Platform: a ground vehicle (UGV), not the drone.** Localisation uncertainty in 3 states is
something you can actually *draw* — you'll watch a thousand particles split into two clumps and
then collapse onto the right one. That picture is worth more than any derivation. It also breaks
you out of UAVs, which is where your Dron-Aid experience already sits. A second UAV capstone
(GPS-denied drone localisation) is available later as a Level 6 side quest.

| # | Lesson | The one idea | You build |
|---|---|---|---|
| 5.1 | The Bayes filter | Kalman is a *special case*. Predict-update on a general belief is the parent of every filter in robotics | Discrete histogram filter — the "robot in a corridor" |
| 5.2 | Motion & measurement models | `p(x_t \| u_t, x_{t-1})` and `p(z_t \| x_t)`. Odometry noise is not Gaussian and pretending it is has consequences | Sampled motion model, banana-shaped uncertainty |
| 5.3 | Particle filter / MCL | When your belief isn't a Gaussian, represent it with a thousand guesses and resample. Solves problems the KF structurally cannot | Monte Carlo localisation |
| 5.4 | Grid maps & a look at SLAM | Occupancy grids; the chicken-and-egg of mapping while localising; what EKF-SLAM and graph-SLAM do | Occupancy grid from range scans |
| **CAP** | **Capstone** | — | **Kidnapped robot: a differential-drive robot in MuJoCo, unknown start pose, known map, noisy range sensor. Localise and drive to a goal.** |

---

### **Level 6 — Optional side quests** (pick any, any time)
- Port the quadcopter to MuJoCo with real aerodynamics
- Unscented Kalman filter, and why it often beats the EKF
- A* / RRT path planning to feed your waypoint executor
- Model Predictive Control on the cart-pole
- **Second capstone: GPS-denied drone localisation** — the UAV counterpart to the Level 5 UGV capstone
- Read one real paper end-to-end, together

---

## 4. What gets built on disk

```
Probabilistic Robotics/
├── README.md                 ← how to use this, start here each session
├── PLAN.md                   ← this file
├── PROGRESS.md               ← your log; where you left off; your own words
├── setup/
│   ├── requirements.txt
│   └── check_setup.py        ← run once; tells you if anything's missing
├── srlib/                    ← the library YOU build, lesson by lesson
│   ├── sim.py                ← integrators, sim loop, timing
│   ├── plotting.py           ← live dashboards, animation, GIF export
│   ├── rotations.py          ← DCM, Euler, Rodrigues
│   ├── sensors.py            ← noisy IMU, GPS, range sensor
│   ├── control.py            ← PID, pole placement, LQR
│   ├── filters.py            ← complementary, KF, EKF, particle
│   └── robots/               ← quad.py, cartpole.py, diffdrive.py
├── level0/ … level5/
│   └── L0.1_numpy_for_robotics/
│       ├── notes.md          ← the lesson: hook, maths, derivation, references
│       ├── lesson.py         ← scaffolding + TODOs
│       ├── test_lesson.py    ← your green light
│       └── sabotage.py       ← the "break it" exercise
├── _solutions/               ← full worked solutions, mirrored structure
├── matlab/                   ← the four cross-check scripts + Simulink models
└── gallery/                  ← GIFs and plots you produce (this is your portfolio)
```

The point of `srlib/` is that **you are building a robotics library, not doing 31 disconnected exercises.** By Level 5 you'll be importing rotation code you wrote in Level 0. That accumulation is what makes it feel like progress instead of homework.

---

## 5. Setup — everything free

**Python 3.11 or 3.12** from [python.org](https://python.org), installed into a **project-local
virtual environment** (`.venv/`). Nothing goes into your system Python.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

The venv matters more than it looks. This course pins particular versions of NumPy, SciPy and
python-control; your MRobotEng papers and anything else you build this year will want different
ones. Keeping them separate is the difference between "my code stopped working and I don't know
why" and never having that problem. It also means a broken environment is a one-minute fix:
delete `.venv/`, rebuild from `requirements.txt`. `.venv/` is gitignored, so it never enters
the repo — anyone cloning it (including future you on another machine) rebuilds it from the
requirements file, which is the point of having one.

`check_setup.py` refuses to pass unless you're actually inside the venv, so this can't go
subtly wrong and surface three lessons later as a mystery import error.

The dependency list, split into two files on purpose:

```
setup/requirements.txt       numpy scipy matplotlib pytest control imageio
setup/requirements-sim.txt   mujoco
```

pip installs a requirements file all-or-nothing, so one package failing to build takes every
other package in that file down with it. There's no reason to let a physics engine you won't
touch until Level 3 block Lesson 0.1 — which is exactly what happened on the first attempt.

`control` is the Python Control Systems Library — the free stand-in for MATLAB's Control System
Toolbox, and what we'll check your hand-written `place()` and `lqr()` against. `mujoco` isn't
needed until Level 3. Full setup, VS Code configuration and troubleshooting live in
`setup/README.md`.

**Why MuJoCo and not PyBullet** (changed 9 September 2026, after the first install attempt
failed): PyBullet's latest release ships no Windows wheels at all, and none for any Python
above 3.11, so on a current Python pip falls back to compiling Bullet from C++ source and
demands the multi-gigabyte Visual C++ build tools. It's been in maintenance mode for years.
MuJoCo is open source under Apache 2.0, actively developed by DeepMind, ships Windows wheels
for Python 3.10–3.14, has a better built-in interactive viewer, and is what robotics research
actually runs on now. The course content doesn't change — only which engine the Level 3 and
Level 5 ports target.

**Editor:** VS Code with the Python extension. Free.
**Version control: GitHub from day one, one commit per lesson.** The commit history is a
deliberate artefact — a recruiter looking at `robotics-from-scratch` sees 31 commits over
however many months, each one a named concept, and that reads as sustained self-directed
learning in a way a finished repo dumped in one commit never does. Message format:

```
LX.Y: <topic> — <what you actually built>
BF0: <what flew>
```

I'll never push anything without asking you first.

**Note on where code runs:** your files live on your machine in this folder. You run them; I read them, review them, and write the lesson material. Nothing needs the cloud.

---

## 6. Reading and watching — short, targeted, all free

I will never send you a 40-hour playlist. Each lesson names at most 1–2 items, usually a single 10-minute video or one book chapter. The recurring sources:

| Source | Used for | Cost |
|---|---|---|
| **[Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python)** (Roger Labbe) | Levels 4–5. Free Jupyter book, intuition-first, no proofs. The best free resource on this topic that exists. | Free |
| **3Blue1Brown — Essence of Linear Algebra** | L0.5 only, episodes 3, 11, 14 | Free |
| **Brian Douglas — Control System Lectures** (YouTube) | L0.8, L3.2–3.4. Short, physical, excellent | Free |
| **Steve Brunton — Control Bootcamp** (YouTube) | L3.1–3.4, when you want it deeper | Free |
| **Russ Tedrake — *Underactuated Robotics*** (MIT, free online textbook) | L3.5 pendulum, L6 MPC | Free |
| **[MuJoCo documentation](https://mujoco.readthedocs.io)** — the Overview and "Modeling" pages | Level 3 port, Level 5 capstone | Free |
| **Thrun/Burgard/Fox — *Probabilistic Robotics*** | Level 5 concepts. The book itself isn't free, but the ideas are well covered by Labbe's book + the authors' lecture slides, which are online. Your university library will have a copy. | See note |

---

## 7. How a study session works

You open a Cowork session, say **"Level 2, lesson 3"** (or just *"next"*), and:

1. I read `PROGRESS.md` to see where you are.
2. Warm-up: 3 retrieval questions in chat.
3. I write `notes.md`, `lesson.py`, `test_lesson.py` into the lesson folder.
4. You read the notes, we discuss the maths in chat until it clicks — interrupt me, argue, ask "but why" as many times as you want. That part is the actual course.
5. You fill in the TODOs, run `pytest`, run the sim.
6. We do predict→run and the sabotage together.
7. You write your 3 sentences in `PROGRESS.md`. Done. Close the laptop.

If you disappear for three weeks, the log picks it up. If you want to skip a lesson because you already know it, take the boss fight instead — pass it and we move on.

---

## 8. What I need from you at each session

Honestly, not much: show up, attempt before looking at solutions, and **tell me when something doesn't make sense instead of nodding along.** The plan collapses if you let a fuzzy concept in Level 0 pass, because Level 4 is built directly on it. Say "I don't get it" early and often — that's the fastest path through this, not the slow one.

---

## 9. Decisions — all settled

| Decision | Choice |
|---|---|
| Toolchain | Python-first; MATLAB/Simulink as a cross-check at L3.1, L3.3–3.4, L4.3 |
| Teaching mode | Fill-in-the-blanks with pytest gates |
| Simulator | Hand-built NumPy through Level 2; MuJoCo from Level 3 onward (was PyBullet; see §5) |
| Python | 3.14 on Windows, in a project-local `.venv` |
| Scope | Full course coverage + Level 5 probabilistic capstone |
| Level 5 platform | Differential-drive UGV. UAV localisation available later as a side quest |
| Version control | GitHub from day one, one commit per lesson |
| Pace | Self-paced, no deadlines |
| Semester interaction | None — no current MRobotEng paper hits state space or estimation, so the level order stands as written |

**PLAN.md is now settled.** Future sessions should follow it, not re-plan it. If something in
here turns out to be wrong once we're building, flag it in a sentence and let Adi decide — no
quiet restructuring.

---

## 10. Which Claude model to use, and when

The plan was designed on Opus. Building the lessons does not need Opus, and this is by design
rather than a compromise — the framework was deliberately built to be **model-robust**:

- Every lesson is gated by pytest checking real mathematical properties. If the generated
  scaffolding is subtly wrong, the tests fail and it gets caught, whichever model wrote it.
- The syllabus, the sequencing and the `srlib` API are already fixed in this document and in
  the stub files. The hard architectural judgement is done; lesson generation is execution
  against a settled spec, which is where Sonnet is strong.

**So: Sonnet at high effort for lesson generation and day-to-day teaching.** Adi is on the Pro
plan and not upgrading, so this is the sustainable choice — the constraint is real, and burning
the weekly allowance on Opus for routine lesson-writing would be the wrong trade.

Worth switching to Opus for, occasionally:

- Boss fights and the Level 5 capstone, where several concepts have to be integrated at once
- A concept that has genuinely refused to click after two attempts on Sonnet — a different
  model often finds a different angle, and it's cheap to try once
- The end-of-level review, where we look back and decide whether anything needs revisiting

Everything else — notes, derivations, scaffolding, tests, debugging, sabotage exercises —
Sonnet. If a lesson comes out shallow or a derivation skips a step, say so and ask for it
again; that is a faster and cheaper fix than defaulting to Opus for everything.

---

## 11. What's already built (as of 9 September 2026)

- `PLAN.md`, `README.md`, `PROGRESS.md`, `PROJECT_INSTRUCTIONS.md`
- `setup/` — `requirements.txt`, `check_setup.py` (run it first; it verifies you're in the venv),
  and `README.md` with venv creation, VS Code configuration and troubleshooting
- `srlib/` — the full library skeleton: every module, class and function signature with
  docstrings explaining what it does and which lesson fills it in. **Deliberately unimplemented.**
  Every body raises `NotImplementedError("L0.2")` and so on — the architecture is given to you,
  the maths is not.
- `conftest.py` — so `import srlib` works from inside any lesson folder
- Empty `level0/`–`level5/`, `_solutions/`, `matlab/`, `gallery/`
- Local git repo, initial commit made, `.gitignore` in place. **Not pushed to GitHub yet** —
  that's Adi's call and Adi's account.

---

**Next step:** new conversation, say *"Lesson 0.1"*. 
