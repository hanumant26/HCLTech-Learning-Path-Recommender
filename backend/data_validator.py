"""
Top-level entrypoint for running data validation script.
"""
import sys
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.data_validator import validate_knowledge_base

if __name__ == "__main__":
    success = validate_knowledge_base()
    sys.exit(0 if success else 1)
