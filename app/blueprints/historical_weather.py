import requests
from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User

historical_bp = Blueprint('historical', __name__, template_folder='../templates')

API_KEY = "YU87AQZC9FSKBEL8GL97CD6K3"
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

@historical_bp.route('/historical-weather', methods=['GET'])
def historical_page():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
        
    return render_template('historical_weather.html', user=user)

@historical_bp.route('/api/historical/fetch', methods=['POST'])
def fetch_historical_json():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json() or {}
    location = payload.get('location', '').strip()
    start_date = payload.get('start_date', '').strip()  
    end_date = payload.get('end_date', '').strip()      

    if not location and user.fishing_region:
        location = user.fishing_region

    if not location or not start_date or not end_date:
        return jsonify({"error": "Missing required coordinates, start date, or end date parameters."}), 400

    try:
        url = f"{BASE_URL}/{location}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&contentType=json"
        response = requests.get(url, timeout=12)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 400:
            return jsonify({"error": f"Invalid query parameters or date range configuration parsed for: '{location}'"}), 400
        else:
            return jsonify({"error": f"VisualCrossing engine error ({response.status_code})"}), response.status_code
            
    except requests.exceptions.RequestException:
        return jsonify({"error": "Connection timeout error contacting historical weather cloud databases."}), 503
