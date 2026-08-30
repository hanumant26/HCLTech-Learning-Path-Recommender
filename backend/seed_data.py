"""
Top-level entrypoint for running database seed script.
"""
import sys
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.seed_data import seed_foundational_data
from backend.app.core.database import SessionLocal, init_db

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_foundational_data(db)
    finally:
        db.close()
