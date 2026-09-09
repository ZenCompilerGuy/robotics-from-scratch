"""
Makes `import srlib` work from inside any lesson folder.

pytest adds the directory containing this file to sys.path, so
`from srlib.rotations import dcm_from_euler` resolves no matter which
level0/L0.7_.../ folder you're running tests from.

You don't need to touch this file.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
