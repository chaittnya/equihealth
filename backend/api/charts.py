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


