import sys
from pathlib import Path

# Add the parent directory to the system path
parent_dir = Path(__file__).resolve().parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))
