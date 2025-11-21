from flask import Blueprint, send_file, request, jsonify
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

def get_color(default=None):
    color = request.args.get("color")
    return color or default

def get_text_color(default="black"):
    color = request.args.get("text_color")
    return color or default


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

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.hist(beds, bins=50, color=color)
    else:
        ax.hist(beds, bins=50)

    ax.set_title(
        "Number of beds vs number of hospitals", color=text_color
    )
    ax.set_xlabel("Number of beds", color=text_color)
    ax.set_ylabel("Number of hospitals", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

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

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.barh(y, num_hospitals, color=color)
    else:
        ax.barh(y, num_hospitals)

    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Number of hospitals", color=text_color)
    ax.set_title(f"Number of hospitals by district", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

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

    y = range(len(districts))
    fig, ax = plt.subplots(figsize=(12, 7))

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.barh(y, total_beds, color=color)
    else:
        ax.barh(y, total_beds)

    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Total beds", color=text_color)
    ax.set_title(f"Total hospital beds by district", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

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

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.barh(y, population, color=color)
    else:
        ax.barh(y, population) 

    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Population", color=text_color)
    ax.set_title(f"District population", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

    fig.tight_layout()
    return fig_to_png_response(fig)


@api_charts.route("/state-district-hospitals-vs-population", methods=["GET"])
def state_district_hospitals_vs_population():
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        return jsonify({"error": "state_id is required"}), 400

    rows = (
        db.session.query(
            District.district_name,
            District.total_persons.label("population"),
            func.count(Hospital.hospital_id).label("num_hospitals")
        )
        .join(Hospital, Hospital.district_id == District.district_id)
        .filter(District.state_id == state_id)
        .group_by(District.district_name, District.total_persons)
        .order_by(District.district_name)
        .all()
    )

    if not rows:
        return jsonify({"error": "No data for given state_id"}), 404

    districts = [r.district_name for r in rows]
    population = [r.population or 0 for r in rows]
    num_hospitals = [r.num_hospitals for r in rows]

    fig, ax = plt.subplots(figsize=(12, 7))

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.scatter(population, num_hospitals, color=color)
    else:
        ax.scatter(population, num_hospitals) 

    ax.set_xlabel("Population", color=text_color)
    ax.set_ylabel("Number of hospitals", color=text_color)
    ax.set_title(f"Hospitals vs population by district", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

    placed_labels = []
    if population:
        x_min, x_max = min(population), max(population)
        y_min, y_max = min(num_hospitals), max(num_hospitals)
        x_range = max(x_max - x_min, 1)
        y_range = max(y_max - y_min, 1)
        x_tol = 0.03 * x_range
        y_tol = 0.03 * y_range

        for name, x, y in zip(districts, population, num_hospitals):
            too_close = False
            for (px, py) in placed_labels:
                if abs(x - px) < x_tol and abs(y - py) < y_tol:
                    too_close = True
                    break

            if too_close:
                continue

            ax.annotate(
                name,
                (x, y),
                textcoords="offset points",
                xytext=(3, 3),
                fontsize=7,
            )
            placed_labels.append((x, y))

    fig.tight_layout()
    return fig_to_png_response(fig)


@api_charts.route("/state-district-bed-ratio", methods=["GET"])
def state_district_bed_ratio():
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        return jsonify({"error": "state_id is required"}), 400

    rows = (
        db.session.query(
            District.district_name,
            District.total_persons.label("population"),
            func.coalesce(func.sum(Hospital.total_beds), 0).label("total_beds")
        )
        .join(Hospital, Hospital.district_id == District.district_id)
        .filter(District.state_id == state_id)
        .group_by(District.district_name, District.total_persons)
        .order_by(District.district_name)
        .all()
    )

    if not rows:
        return jsonify({"error": "No data for given state_id"}), 404

    districts = []
    ratios = []

    for r in rows:
        pop = r.population or 0
        beds = r.total_beds or 0
        if pop > 0:
            ratio = beds * 10000.0 / pop
        else:
            ratio = 0
        districts.append(r.district_name)
        ratios.append(ratio)

    y = range(len(districts))
    fig, ax = plt.subplots(figsize=(12, 7))

    color = get_color()
    text_color = get_text_color()
    if color:
        ax.barh(y, ratios, color=color)
    else:
        ax.barh(y, ratios)

    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.invert_yaxis()
    ax.set_xlabel("Beds per 10,000 people", color=text_color)
    ax.set_title(f"Hospital bed availability ratio by district", color=text_color)
    plt.setp(ax.get_xticklabels(), color=text_color)
    plt.setp(ax.get_yticklabels(), color=text_color)

    fig.tight_layout()
    return fig_to_png_response(fig)
