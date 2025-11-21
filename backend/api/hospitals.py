from flask import Blueprint, jsonify, request
from extensions import db
from models import State, District, Hospital
from sqlalchemy.orm import joinedload

api_hospitals = Blueprint("hospitals", __name__, url_prefix="/api/hospitals")


def serialize_hospital(h):
    return {
        **h.to_dict(),
        "state": h.state.to_dict() if h.state else None,
        "district": h.district.to_dict() if h.district else None,
        "categories": [c.to_dict() for c in (h.categories or [])],
    }


def fetch_hospitals(state_id=None, district_id=None, hospital_id=None):
    query = (
        Hospital.query
        .options(
            joinedload(Hospital.state),
            joinedload(Hospital.district),
            joinedload(Hospital.categories),
        )
    )
    if state_id is not None:
        query = query.filter_by(state_id=state_id)

    if district_id is not None:
        query = query.filter_by(district_id=district_id)

    if hospital_id is not None:
        query = query.filter_by(hospital_id=hospital_id)

    return query.order_by(Hospital.hospital_name.asc()).all()


# GET /api/hospitals/compact
# PReturn a compact list of hospitals filtered by state_id and optionally by district_id and/or hospital_id.
# Query:
#   - state_id    (int, required): State to filter by.
#   - district_id (int, optional): District to filter by (within the state).
#   - hospital_id (int, optional): Specific hospital ID.
@api_hospitals.route("/compact", methods=["GET"])
def get_hospitals_compact():
    state_id = request.args.get("state_id", type=int)
    district_id = request.args.get("district_id", type=int)
    hospital_id = request.args.get("hospital_id", type=int)

    query = (
        Hospital.query
        .filter_by(state_id=state_id)
    )

    if district_id is not None:
        query = query.filter_by(district_id=district_id)

    if hospital_id is not None:
        query = query.filter_by(hospital_id=hospital_id)

    hospitals = query.order_by(Hospital.hospital_name.asc()).all()

    return jsonify({
        "count": len(hospitals),
        "data": [h.to_dict() for h in hospitals]
    }), 200


# GET /api/hospitals
# Return hospitals filtered by state_id and optionally district_id and/or hospital_id.
# Query:
#   - state_id    (int, optional): State filter; if omitted, behavior depends on fetch_hospitals.
#   - district_id (int, optional): District filter.
#   - hospital_id (int, optional): Specific hospital ID.
@api_hospitals.route("/", methods=["GET"])
def get_hospitals():
    state_id = request.args.get("state_id", type=int) # defailt None
    district_id = request.args.get("district_id", type=int)
    hospital_id = request.args.get("hospital_id", type=int)

    hospitals = fetch_hospitals(state_id, district_id, hospital_id)

    if not hospitals:
        return jsonify({"message": f"No hospitals found for state_id {state_id}, district_id {district_id}, hospital_id {hospital_id}"}), 404

    data = [serialize_hospital(h) for h in hospitals]
    return jsonify({"count": len(data), "data": data}), 200


# GET /api/hospitals/grouped
# Return hospitals grouped hierarchically: state → districts → hospitals.
# Ensures states and districts appear even when no hospitals exist in that district.
# Query:
#   - state_id    (int, optional): If omitted, include all states.
#   - district_id (int, optional): Restrict to this district (optional).
@api_hospitals.route("/grouped/", methods=["GET"])
def get_grouped_hospitals():
    state_id = request.args.get("state_id", type=int)
    district_id = request.args.get("district_id", type=int)

    # Fetch all states (apply filter if state_id provided)
    state_query = State.query
    if state_id:
        state_query = state_query.filter(State.state_id == state_id)

    states = state_query.order_by(State.state_name).all()

    if not states:
        return jsonify({"message": "No states found", "count": 0, "data": []}), 404

    # Fetch all districts for the selected states (apply filters if given)
    district_query = District.query
    if state_id:
        district_query = district_query.filter(District.state_id == state_id)
    if district_id:
        district_query = district_query.filter(District.district_id == district_id)

    districts = district_query.order_by(District.district_name).all()

    # Fetch hospitals joined with state and district (filtered if specified)
    hospital_query = (
        Hospital.query
        .options(
            joinedload(Hospital.state).undefer('*'),
            joinedload(Hospital.district).undefer('*')
        )
        .order_by(Hospital.hospital_name)
    )

    if state_id:
        hospital_query = hospital_query.filter(Hospital.state_id == state_id)
    if district_id:
        hospital_query = hospital_query.filter(Hospital.district_id == district_id)

    hospitals = hospital_query.all()

    # Initialize state map
    state_map = {
        s.state_id: {
            **s.to_dict(),
            "districts": {}
        }
        for s in states
    }

    # Initialize district entries for each state even if no hospitals exist
    for d in districts:
        if d.state_id in state_map:
            state_map[d.state_id]["districts"][d.district_id] = {
                **d.to_dict(),
                "hospitals": [],
                "count": 0
            }

    # Assign hospitals to correct district
    for h in hospitals:
        s_id = h.state_id
        d_id = h.district_id

        if s_id in state_map and d_id in state_map[s_id]["districts"]:
            entry = state_map[s_id]["districts"][d_id]
            entry["hospitals"].append(h.to_dict())
            entry["count"] += 1

    # Convert dicts to lists and add district counts
    result = []
    for s in state_map.values():
        s["districts"] = list(s["districts"].values())
        s["count"] = len(s["districts"])
        result.append(s)

    return jsonify({"count": len(result), "data": result}), 200
