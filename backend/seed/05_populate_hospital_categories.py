import os
import sys
import csv

# --- Ensure parent directory (project root) is importable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import Hospital, Category, State, hospital_category

CSV_FILE = "../data/maharashtra/hospital_category.csv"
DEFAULT_STATE_NAME = "Maharashtra"   # default for all hospitals in this file


def clean_int(v):
    try:
        if v is None or str(v).strip() == "":
            return None
        return int(float(v))
    except Exception:
        return None


def populate_hospital_categories():
    with app.app_context():
        # Resolve state_id once
        state = State.query.filter_by(state_name=DEFAULT_STATE_NAME).first()
        if not state:
            raise RuntimeError(f"State '{DEFAULT_STATE_NAME}' not found. Insert it first.")
        state_id = state.state_id

        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            inserted, skipped_missing, skipped_duplicate = 0, 0, 0

            for row in reader:
                hospital_id = clean_int(row.get("hospital_id"))
                category_id = clean_int(row.get("category_id"))

                if hospital_id is None or category_id is None:
                    print(f"Skipping row with missing ids: {row}")
                    skipped_missing += 1
                    continue

                # Check existence of hospital & category
                hospital = Hospital.query.get((hospital_id, state_id))
                category = Category.query.get(category_id)

                if not hospital:
                    print(f"Skipping: Hospital ({hospital_id}, state_id={state_id}) not found.")
                    skipped_missing += 1
                    continue
                if not category:
                    print(f"Skipping: Category {category_id} not found.")
                    skipped_missing += 1
                    continue

                # Duplicate check in association table
                existing = db.session.execute(
                    db.select(hospital_category).filter_by(
                        hospital_id=hospital_id,
                        state_id=state_id,
                        category_id=category_id,
                    )
                ).first()

                if existing:
                    print(f"Skipping existing link: Hospital {hospital_id} (state {state_id}) ↔ Category {category_id}")
                    skipped_duplicate += 1
                    continue

                # Insert relationship
                db.session.execute(
                    hospital_category.insert().values(
                        hospital_id=hospital_id,
                        state_id=state_id,
                        category_id=category_id,
                    )
                )
                inserted += 1

            db.session.commit()
            print("Hospital–Category associations populated successfully!")
            print(f"Inserted: {inserted}")
            print(f"Skipped (missing hospital/category): {skipped_missing}")
            print(f"Skipped (duplicates): {skipped_duplicate}")


if __name__ == "__main__":
    populate_hospital_categories()
