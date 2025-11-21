from flask import Blueprint, send_file, request
from io import BytesIO

import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from extensions import db
from models import State, District, Hospital
from sqlalchemy import func

api_charts = Blueprint("api_charts", __name__, url_prefix="/api/charts")

# Convert a Matplotlib figure to a Flask Response (image/png),
# without saving to disk.
def fig_to_png_response(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


# 1) Histogram of number of beds per hospital
# GET /api/charts/beds
@api_charts.route("/beds", methods=["GET"])
def beds():
    rows = (
        db.session.query(Hospital.total_beds)
        .filter(Hospital.total_beds.isnot(None))
        .all()
    )
    beds = [r.total_beds for r in rows if r.total_beds is not None]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(beds, bins=50)
    ax.set_title(
        "Histogram plot of number of buckets as number of beds.\n"
        "Counts the number of hospitals within that bucket of beds."
    )
    ax.set_xlabel("Number of beds")
    ax.set_ylabel("Number of hospitals")

    return fig_to_png_response(fig)


@api_charts.route("/state-district-hospitals", methods=["GET"])
def state_district_hospitals():
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        return jsonify({"error": "state_id is required"}), 400

    rows = (
        db.session.query(
            District.district_name,
            func.count(Hospital.hospital_id).label("num_hospitals")
        )
        .join(Hospital, Hospital.district_id == District.district_id)
        .filter(District.state_id == state_id)
        .group_by(District.district_name)
        .order_by(District.district_name)
        .all()
    )

    if not rows:
        return jsonify({"error": "No data for given state_id"}), 404

    districts = [r.district_name for r in rows]
    num_hospitals = [r.num_hospitals for r in rows]

    y = range(len(districts))
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(y, num_hospitals)
    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Number of hospitals")
    ax.set_title(f"Number of hospitals by district")

    fig.tight_layout()
    return fig_to_png_response(fig)

@api_charts.route("/state-district-beds", methods=["GET"])
def state_district_beds():
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        return jsonify({"error": "state_id is required"}), 400

    rows = (
        db.session.query(
            District.district_name,
            func.coalesce(func.sum(Hospital.total_beds), 0).label("total_beds")
        )
        .join(Hospital, Hospital.district_id == District.district_id)
        .filter(District.state_id == state_id)
        .group_by(District.district_name)
        .order_by(District.district_name)
        .all()
    )

    if not rows:
        return jsonify({"error": "No data for given state_id"}), 404

    districts = [r.district_name for r in rows]
    total_beds = [r.total_beds for r in rows]

    # horizontal bar chart for readability
    y = range(len(districts))
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(y, total_beds)
    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()  # highest at top
    ax.set_xlabel("Total beds")
    ax.set_title(f"Total hospital beds by district")

    fig.tight_layout()
    return fig_to_png_response(fig)


@api_charts.route("/state-district-population", methods=["GET"])
def state_district_population():
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        return jsonify({"error": "state_id is required"}), 400

    rows = (
        db.session.query(
            District.district_name,
            District.total_persons.label("population")
        )
        .filter(District.state_id == state_id)
        .order_by(District.district_name)
        .all()
    )

    if not rows:
        return jsonify({"error": "No data for given state_id"}), 404

    districts = [r.district_name for r in rows]
    population = [r.population or 0 for r in rows]

    y = range(len(districts))
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(y, population)
    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Population")
    ax.set_title(f"District population (state_id={state_id})")

    fig.tight_layout()
    return fig_to_png_response(fig)
