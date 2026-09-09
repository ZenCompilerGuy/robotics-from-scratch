# Setup

Everything for this course lives in a **virtual environment** — a private copy of Python and
its packages that belongs to this project alone. Nothing gets installed into your system Python.

Why it's worth the two extra commands: this course pins specific versions of NumPy, SciPy and
python-control. Your MRobotEng papers, or anything else you build this year, will want different
ones. A venv means those never collide, and if this environment ever gets into a broken state
you delete one folder and rebuild it in a minute.

`.venv/` is in `.gitignore`, so it never gets committed. It's yours, not part of the repo —
which is why anyone cloning this repo (including future you, on another machine) recreates it
from `requirements.txt` rather than downloading it.

---

## First time

From the repo root:

### Windows — PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

### Windows — cmd

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r setup/requirements.txt
python setup/check_setup.py
```

`check_setup.py` will tell you if you're not actually in the venv, so you can't get this
subtly wrong and only find out three lessons later.

The 3D physics engine is **not** in `requirements.txt` — it's in `requirements-sim.txt` and
isn't needed until Level 3. Install it when you get there:

```powershell
python -m pip install -r setup/requirements-sim.txt
```

Keeping them separate is deliberate: pip installs a requirements file all-or-nothing, so one
package failing to build takes the other six down with it. No reason to let a simulator you
won't touch for months block Lesson 0.1.

---

## Every session after that

Just activate it. One line, from the repo root:

```powershell
.venv\Scripts\Activate.ps1        # Windows PowerShell
```
```bash
source .venv/bin/activate          # macOS / Linux
```

Your prompt gets a `(.venv)` prefix. That prefix is the whole tell — if it's not there, you're
in the wrong Python, and `pytest` will fail with import errors that look like your code is
broken when it isn't.

`deactivate` when you're done, or just close the terminal.

---

## VS Code

Do this once and VS Code handles activation for you in every new terminal:

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose the one whose path contains `.venv` — it's usually labelled *(Recommended)*

Then the Run button, the debugger and the Testing panel all use the venv automatically.
To get the green tick marks next to your lesson tests: `Ctrl+Shift+P` → **Python: Configure
Tests** → **pytest** → select the repo root.

---

## Troubleshooting

**`Activate.ps1 cannot be loaded because running scripts is disabled on this system`**

Windows blocks PowerShell scripts by default. Fix it once, for your user account only:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again. (`RemoteSigned` still blocks unsigned scripts downloaded from the internet
— it only trusts ones you wrote locally, which is what `.venv` is. This is the recommendation
in Microsoft's own venv documentation, not a workaround.)

**`python` isn't recognised, or opens the Microsoft Store**

Python isn't on PATH. Reinstall from python.org with **"Add python.exe to PATH"** ticked at the
bottom of the first installer screen. Try `py -3` in the meantime.

**`pytest` says `ModuleNotFoundError: No module named 'srlib'`**

You're not in the venv, or you're running pytest from the wrong directory. Check for the
`(.venv)` prefix, and run pytest from the repo root — `conftest.py` there is what makes
`import srlib` resolve.

**`error: Microsoft Visual C++ 14.0 or greater is required` / `Failed building wheel for <x>`**

pip couldn't find a prebuilt wheel for your Python version, so it fell back to compiling the
package from C++ source — and that needs a compiler you don't have. Two things to know:

*Don't install the Visual C++ Build Tools to fix this.* They're several gigabytes and it's
almost always the wrong answer. A missing wheel means the package doesn't support your Python
version yet, and compiling it yourself is a fragile workaround, not a fix.

*The right fix is to check whether the package supports your Python at all.* Look at the
package's PyPI "Download files" page for a wheel matching your version — `cp314` for Python
3.14, `cp312` for 3.12, or `py3-none-any` which works everywhere. If there isn't one, either
the package needs a newer release or you need a different package. This is exactly what
happened with PyBullet on this course, and why we use MuJoCo instead (see
`requirements-sim.txt`).

Check your version with `python --version`. Running a very new Python — 3.14 was released
recently — means occasionally arriving before a package does.

**Everything's broken and you want a clean slate**

Delete the `.venv` folder and redo the first-time steps. You lose nothing; none of your work
lives in there.

---

## Alternatives

If you already use **conda** and prefer it, `conda create -n robotics python=3.12` then
`pip install -r setup/requirements.txt` works identically — the course doesn't care which tool
made the environment, only that there is one. Just don't run both.
