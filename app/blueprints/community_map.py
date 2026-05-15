from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User, db
from app.models.community_pin import CommunityPin

community_map_bp = Blueprint('community_map', __name__, template_folder='../templates')

@community_map_bp.route('/community-map', methods=['GET'])
def view_community_map():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    return render_template('community_map.html', user=user)

@community_map_bp.route('/api/community/pins', methods=['GET'])
def get_global_pins():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    pins = CommunityPin.query.order_by(CommunityPin.created_at.desc()).all()
    
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
            "creator_name": p.creator.display_name or p.creator.username if p.creator else "Anonymous", # Pull username
            "conditions": {
                "pressure": p.pressure or "N/A",
                "cloud": p.cloud_cover or "N/A",
                "rain": p.rain or "N/A",
                "temp": p.temp or "N/A",
                "wind": p.wind or "N/A"
            }
        })
    return jsonify({"pins": pins_data})

@community_map_bp.route('/api/community/pins/create', methods=['POST'])
def save_community_pin():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    data = request.get_json() or {}
    
    name = data.get('spot_name', '').strip()
    lat = data.get('latitude')
    lng = data.get('longitude')
    
    if not name or lat is None or lng is None:
        return jsonify({"error": "Missing pin coordinates or location name parameters."}), 400
        
    p = CommunityPin(
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

@community_map_bp.route('/api/community/pins/delete/<int:pin_id>', methods=['DELETE'])
def admin_delete_pin(pin_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    if int(session['user_id']) != 1:
        return jsonify({"error": "Forbidden: Only administrative master profiles can clear community map pins."}), 403
        
    p = CommunityPin.query.get(pin_id)
    if not p:
        return jsonify({"error": "Target pin location does not exist inside global logs."}), 404
        
    db.session.delete(p)
    db.session.commit()
    return jsonify({"success": True})
