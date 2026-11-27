import sys
from pathlib import Path

# Tests import the package from the checkout, and each other's helpers.
sys.path[:0] = [str(Path(__file__).parent.parent), str(Path(__file__).parent)]
