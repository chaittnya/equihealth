import csv
import os
import sys

# Ensure we can import app + models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import Hospital, State, District

# --- Config ---
CSV_FILE = "../data/maharashtra/hospital.csv"
DEFAULT_STATE_NAME = "Maharashtra"  # change if importing another state


def clean_str(value):
    """Convert floats like '400701.0' to '400701', trim, return None for blanks."""
    if value is None:
        return None
    s = str(value).strip()
    if s in ("", "nan", "NaN", "None"):
        return None
    if s.endswith(".0"):
        s = s[:-2]
    return s


def clean_int(value):
    """Safely convert numeric-looking strings to int or None."""
    try:
        if value is None or str(value).strip() == "":
            return None
        return int(float(value))
    except Exception:
        return None


def clean_float(value):
    """Safely convert to float or return None."""
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def populate_hospitals():
    with app.app_context():
        # Resolve state_id from name
        state = State.query.filter_by(state_name=DEFAULT_STATE_NAME).first()
        if not state:
            raise RuntimeError(f"State '{DEFAULT_STATE_NAME}' not found. Insert it first.")
        state_id = state.state_id

        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count_inserted = 0
            count_skipped = 0
            count_bad_district = 0

            for row in reader:
                hospital_id = clean_int(row.get("hospital_id"))
                district_id = clean_int(row.get("district_id"))

                if hospital_id is None:
                    print(f"Skipping row with missing hospital_id: {row}")
                    count_skipped += 1
                    continue

                # Composite PK check: (hospital_id, state_id)
                existing = Hospital.query.filter_by(
                    hospital_id=hospital_id,
                    state_id=state_id
                ).first()

                if existing:
                    print(f"Skipping existing hospital ID {hospital_id} ({existing.hospital_name})")
                    count_skipped += 1
                    continue

                # Optional validation: if district_id provided, ensure it exists and belongs to the same state
                if district_id is not None:
                    d = District.query.filter_by(district_id=district_id).first()
                    if not d or d.state_id != state_id:
                        print(f"Skipping hospital ID {hospital_id}: district_id {district_id} "
                              f"missing or belongs to different state (expected state_id={state_id}).")
                        count_bad_district += 1
                        continue

                hospital = Hospital(
                    hospital_id=hospital_id,
                    state_id=state_id,
                    district_id=district_id,
                    hospital_name=(row.get("hospital_name") or "").strip(),
                    address=(row.get("address") or "").strip() or None,
                    pincode=clean_str(row.get("pincode")),
                    latitude=clean_float(row.get("latitude")),
                    longitude=clean_float(row.get("longitude")),
                    mco_contact_number=clean_str(row.get("mco_contact_number")),
                    total_beds=clean_int(row.get("total_beds")),
                    hospital_type=(row.get("hospital_type") or "").strip() or None,
                    government_subtype=(row.get("government_subtype") or "").strip() or None,
                )

                db.session.add(hospital)
                count_inserted += 1

            db.session.commit()

            print("Hospitals table populated successfully!")
            print(f"Inserted: {count_inserted}")
            print(f"Skipped (duplicates/invalid rows): {count_skipped}")
            print(f"Skipped (bad or cross-state district): {count_bad_district}")


if __name__ == "__main__":
    populate_hospitals()
