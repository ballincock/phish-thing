from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User, db
from app.models.spot_pin import SpotPin

map_log_bp = Blueprint('map_log', __name__, template_folder='../templates')

@map_log_bp.route('/map-log', methods=['GET'])
def view_map():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    return render_template('maps/private/map_log.html', user=user)

@map_log_bp.route('/api/pins', methods=['GET'])
def get_user_pins():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']

    pins = SpotPin.query.filter_by(user_id=uid).order_by(SpotPin.created_at.desc()).all()

    pins_data = []
    for p in pins:
        pins_data.append({
            "id": p.id,
            "name": p.spot_name,
            "lat": p.latitude,
            "lng": p.longitude,
            "species": p.species or "N/A",
            "lure": p.lure_used or "N/A",
            "season": p.time_of_year or "Unknown",
            "conditions": {
                "pressure": p.pressure or "N/A",
                "cloud": p.cloud_cover or "N/A",
                "rain": p.rain or "N/A",
                "temp": p.temp or "N/A",
                "wind": p.wind or "N/A"
            }
        })
    return jsonify({"pins": pins_data})

@map_log_bp.route('/api/pins/create', methods=['POST'])
def save_new_pin():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    data = request.get_json() or {}

    name = data.get('spot_name', '').strip()
    lat = data.get('latitude')
    lng = data.get('longitude')

    if not name or lat is None or lng is None:
        return jsonify({"error": "Missing pin placement coordinates or spot name metadata."}), 400

    p = SpotPin(
        user_id=uid,
        spot_name=name,
        latitude=float(lat),
        longitude=float(lng),
        species=data.get('species'),
        lure_used=data.get('lure_used'),
        time_of_year=data.get('time_of_year'),
        pressure=data.get('pressure'),
        cloud_cover=data.get('cloud_cover'),
        rain=data.get('rain'),
        temp=data.get('temp'),
        wind=data.get('wind')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"success": True, "pin_id": p.id})

@map_log_bp.route('/api/pins/delete/<int:pin_id>', methods=['DELETE'])
def delete_user_pin(pin_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    p = SpotPin.query.filter_by(id=pin_id, user_id=session['user_id']).first()

    if not p:
        return jsonify({"error": "Resource forbidden or location pin does not exist."}), 403

    db.session.delete(p)
    db.session.commit()
    return jsonify({"success": True})
