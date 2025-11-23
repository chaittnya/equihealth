import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import Category

# Path to your CSV file
CSV_FILE = "../data/maharashtra/category.csv"

def populate_categories():
    with app.app_context():
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Check if category already exists
                existing = Category.query.filter_by(category_id=row["category_id"]).first()
                if existing:
                    print(f"Skipping existing category ID {row['category_id']}: {row['category_name']}")
                    continue

                # Create a new Category object
                category = Category(
                    category_id=int(row["category_id"]),
                    category_name=row["category_name"].strip()
                )
                db.session.add(category)

            db.session.commit()
            print("Categories table populated successfully!")

if __name__ == "__main__":
    populate_categories()
