import os
import sys
import csv

# --- Ensure parent directory (project root) is importable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import State

# Path to your CSV file
CSV_FILE = "../data/India States-UTs.csv"


def clean_str(value):
    """Trim and handle blank/NaN strings."""
    if not value or str(value).strip() in ("", "nan", "NaN", "None"):
        return None
    return str(value).strip()


def clean_float(value):
    """Safely convert to float or return None."""
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def populate_states():
    with app.app_context():
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count_inserted, count_skipped = 0, 0

            for idx, row in enumerate(reader, start=1):
                state_name = clean_str(row.get("State/UT"))
                latitude = clean_float(row.get("Latitude"))
                longitude = clean_float(row.get("Longitude"))

                if not state_name:
                    print(f"Skipping row {idx}: Missing state name.")
                    count_skipped += 1
                    continue

                # Check if state already exists
                existing = State.query.filter_by(state_name=state_name).first()
                if existing:
                    print(f"Skipping existing state: {state_name}")
                    count_skipped += 1
                    continue

                # Create new state entry
                state = State(
                    state_name=state_name,
                    latitude=latitude,
                    longitude=longitude
                )

                db.session.add(state)
                count_inserted += 1

            db.session.commit()

            print("\nStates table populated successfully!")
            print(f"Inserted: {count_inserted}")
            print(f"Skipped (duplicates/missing): {count_skipped}")


if __name__ == "__main__":
    populate_states()
