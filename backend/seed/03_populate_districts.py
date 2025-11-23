import csv
import os
import sys

# Ensure we can import app + models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import District, State

# Path to your CSV file
CSV_FILE = "../data/maharashtra/district.csv"
DEFAULT_STATE_NAME = "Maharashtra" 

def clean_str(value):
    if not value or str(value).strip() in ("", "nan", "NaN", "None"):
        return None
    return str(value).strip()


def clean_int(value):
    try:
        if value is None or str(value).strip() == "":
            return None
        return int(float(value))
    except Exception:
        return None


def clean_float(value):
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def populate_districts():
    with app.app_context():
        state = State.query.filter_by(state_name=DEFAULT_STATE_NAME).first()
        if not state:
            raise RuntimeError(f"State '{DEFAULT_STATE_NAME}' not found. Insert it first.")
        state_id = state.state_id
        
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count_inserted, count_skipped, count_missing_state = 0, 0, 0

            for row in reader:
                district_id = clean_int(row.get("district_id"))
                district_name = clean_str(row.get("district_name")) 
                

                if district_id is None or district_name is None or state_id is None:
                    print(f"Skipping row with missing required fields: {row}")
                    count_skipped += 1
                    continue

                # Ensure referenced state exists; otherwise skip (FK would fail)
                if not State.query.filter_by(state_id=state_id).first():
                    print(f"Skipping district ID {district_id}: missing state_id={state_id}")
                    count_missing_state += 1
                    continue

                # Check for existing district by PK
                existing = District.query.filter_by(district_name=district_name, state_id=state_id).first()
                if existing:
                    print(f"Skipping existing district ID  {district_id} ({existing.district_name}) in state id {state}")
                    count_skipped += 1
                    continue

                district = District(
                    district_id=district_id,
                    district_name=district_name,
                    state_id=state_id,
                    latitude=clean_float(row.get("latitude")),
                    longitude=clean_float(row.get("longitude")),
                    total_persons=clean_int(row.get("total_persons")),
                    total_males=clean_int(row.get("total_males")),
                    total_females=clean_int(row.get("total_females")),
                    children_persons=clean_int(row.get("children_persons")),
                    children_males=clean_int(row.get("children_males")),
                    children_females=clean_int(row.get("children_females")),
                )

                db.session.add(district)
                count_inserted += 1

            db.session.commit()

            print("Districts table populated successfully!")
            print(f"Inserted: {count_inserted}")
            print(f"Skipped (duplicates/invalid): {count_skipped}")
            print(f"Skipped (missing state): {count_missing_state}")


if __name__ == "__main__":
    populate_districts()
