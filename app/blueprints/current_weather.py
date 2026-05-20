import requests
from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User

weather_bp = Blueprint('weather', __name__, template_folder='../templates')

API_KEY = "YU87AQZC9FSKBEL8GL97CD6K3"
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

@weather_bp.route('/weather', methods=['GET'])
def weather_page():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
        
    return render_template('weather/current_weather.html', user=user)

@weather_bp.route('/api/weather/fetch', methods=['POST'])
def fetch_weather_json():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json() or {}
    location = payload.get('location', '').strip()

    if not location and user.fishing_region:
        location = user.fishing_region

    if not location:
        return jsonify({"error": "No specific region parsing parameter submitted."}), 400

    try:
        url = f"{BASE_URL}/{location}?unitGroup=metric&key={API_KEY}&contentType=json"
        response = requests.get(url, timeout=10)
    
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 400:
            return jsonify({"error": f"Invalid target destination input: '{location}'"}), 400
        else:
            return jsonify({"error": f"VisualCrossing processing error ({response.status_code})"}), response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"Network Connection Debug Error: {e}") 
        return jsonify({"error": "Connection timeout error contacting API cloud engines."}), 503
