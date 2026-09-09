"""
Run me first — from inside the activated virtual environment:

    python setup/check_setup.py

Tells you whether you're in the venv, what's installed, what's missing, and
the one command that fixes it. Safe to run any time.
"""
import os
import sys
import subprocess
import shutil

MIN_PY = (3, 10)

# (import name, pip name, what it's for, required?)
PACKAGES = [
    ("numpy",      "numpy",      "arrays, linear algebra — every single lesson", True),
    ("scipy",      "scipy",      "solving Riccati equations for LQR (Level 3)", True),
    ("matplotlib", "matplotlib", "every plot and animation you'll make", True),
    ("pytest",     "pytest",     "the green light on each lesson", True),
    ("control",    "control",    "free stand-in for MATLAB's Control System Toolbox (Level 3)", True),
    ("imageio",    "imageio",    "exporting animations as GIFs for your gallery/portfolio", True),
    ("pybullet",   "pybullet",   "3D physics engine (Level 3 onward)", False),
    ("jupyter",    "jupyter",    "notebooks, if you prefer them to plain scripts", False),
]

GREEN, RED, YELLOW, DIM, BOLD, RESET = (
    "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[1m", "\033[0m"
)


def in_virtualenv() -> bool:
    """True if this interpreter is a venv/virtualenv, not the system Python."""
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def activate_hint() -> str:
    """The right activation command for whatever shell we appear to be in."""
    if os.name == "nt":
        return r".venv\Scripts\Activate.ps1      (PowerShell)   or   .venv\Scripts\activate.bat  (cmd)"
    return "source .venv/bin/activate"


def main() -> int:
    print(f"\n{BOLD}Robotics from Scratch — environment check{RESET}\n")

    ok = True
    missing_required, missing_optional = [], []

    # --- Virtual environment --------------------------------------------
    venv = in_virtualenv()
    if venv:
        print(f"  {GREEN}OK{RESET}   virtual environment active")
        print(f"       {DIM}{sys.prefix}{RESET}")
    else:
        ok = False
        print(f"  {RED}NO{RESET}   NOT in a virtual environment — this is the system Python")
        print(f"       {DIM}Installing course packages here pollutes your global Python{RESET}")

    # --- Python version -------------------------------------------------
    print()
    v = sys.version_info
    if (v.major, v.minor) >= MIN_PY:
        print(f"  {GREEN}OK{RESET}   Python {v.major}.{v.minor}.{v.micro}")
    else:
        ok = False
        print(f"  {RED}NO{RESET}   Python {v.major}.{v.minor} — need {MIN_PY[0]}.{MIN_PY[1]} or newer")
    print(f"       {DIM}{sys.executable}{RESET}")

    # --- Packages -------------------------------------------------------
    print()
    for import_name, pip_name, purpose, required in PACKAGES:
        try:
            mod = __import__(import_name)
            version = getattr(mod, "__version__", "?")
            print(f"  {GREEN}OK{RESET}   {import_name:<12} {version:<10} {DIM}{purpose}{RESET}")
        except ImportError:
            if required:
                ok = False
                missing_required.append(pip_name)
                print(f"  {RED}NO{RESET}   {import_name:<12} {'':<10} {DIM}{purpose}{RESET}")
            else:
                missing_optional.append(pip_name)
                print(f"  {YELLOW}--{RESET}   {import_name:<12} {'optional':<10} {DIM}{purpose}{RESET}")

    # --- git ------------------------------------------------------------
    print()
    if shutil.which("git"):
        try:
            ver = subprocess.run(
                ["git", "--version"], capture_output=True, text=True, timeout=10
            ).stdout.strip()
            print(f"  {GREEN}OK{RESET}   {ver}")
        except Exception:
            print(f"  {GREEN}OK{RESET}   git found")
    else:
        ok = False
        print(f"  {RED}NO{RESET}   git — install from https://git-scm.com/downloads")

    # --- Verdict --------------------------------------------------------
    print()

    if not venv:
        print(f"{RED}{BOLD}Fix this first — create and activate the venv:{RESET}\n")
        print("    python -m venv .venv")
        print(f"    {activate_hint()}")
        print("    python -m pip install -r setup/requirements.txt")
        print("    python setup/check_setup.py\n")
        print(f"{DIM}Ignore the package list above until you're in the venv — that's your")
        print(f"system Python's packages, not the course's.{RESET}\n")
        return 1

    if missing_required:
        print(f"{RED}Missing required packages.{RESET} Run this:\n")
        print(f"    python -m pip install {' '.join(missing_required)}\n")
    if missing_optional:
        print(f"{YELLOW}Optional, install when you reach Level 3:{RESET}\n")
        print(f"    python -m pip install {' '.join(missing_optional)}\n")

    if ok and not missing_required:
        print(f"{GREEN}{BOLD}All good. You're ready for Lesson 0.1.{RESET}\n")
        return 0

    print(f"{DIM}Fix the above and run this script again.{RESET}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
