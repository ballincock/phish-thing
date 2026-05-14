import requests
from datetime import datetime
from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User
from app.models.weather_log import ApiWeatherLog
from app.models.user import db

predictions_bp = Blueprint('predictions', __name__, template_folder='../templates')

API_KEY = "YU87AQZC9FSKBEL8GL97CD6K3"
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

@predictions_bp.route('/weather-predictions', methods=['GET'])
def predictions_page():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
        
    return render_template('weather_predictions.html', user=user)

@predictions_bp.route('/api/predictions/fetch', methods=['POST'])
def fetch_predictions_json():
    global db
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json() or {}
    city = payload.get('city_input', '').strip()
    target_species = payload.get('target_species', 'Bass')

    if not city:
        return jsonify({"error": "No valid target city provided. Please enter a location name."}), 400

    url = f"{BASE_URL}/{city}/today"
    params = {"unitGroup": "us", "key": API_KEY, "include": "current", "contentType": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        weather_json = response.json()
        current = weather_json.get('currentConditions', {})
        
        temp = current.get('temp', 0)
        pressure = current.get('pressure', 1013)
        precip = current.get('precip', 0)
        w_speed = current.get('windspeed', 0)
        w_dir_deg = current.get('winddir', 0)
        humidity = current.get('humidity', 50)
        moon_phase = current.get('moonphase', 0)

        dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        w_dir = dirs[int((w_dir_deg + 22.5) % 360 / 45)]

        # Base ORM Logging
        log_entry = ApiWeatherLog(
            location=city,
            temp=float(temp or 0),
            pressure=float(pressure or 1013),
            precip=float(precip or 0),
            wind_speed=float(w_speed or 0),
            wind_dir=w_dir
        )
        db.session.add(log_entry)
        db.session.commit()

        rows = ApiWeatherLog.query.order_by(ApiWeatherLog.id.desc()).limit(5).all()
        history_list = [{"city": r.location, "temp": r.temp, "time": r.logged_at.strftime('%H:%M:%S')} for r in rows]

        front_verdict = "Stationary / Stable Air"
        wind_shift_alert = "Consistent Flows"
        precip_potential = "Low Probability"
        barometer_trend = "Steady"

        if pressure < 1005:
            front_verdict = "Occluded Front (Low-Pressure Cyclone Enclosure)"
            barometer_trend = "Falling / Unstable"
        elif 1005 <= pressure <= 1012:
            front_verdict = "Active Frontal Boundary (Developing System)"
            barometer_trend = "Fluctuating"
        elif pressure > 1022:
            barometer_trend = "Rising High Pressure"

        if w_dir in ['NW', 'N'] and temp < 55:
            front_verdict = "Cold Frontal Passage Active"
            wind_shift_alert = "Clocking shift to Northern quadrant (Cold Air Advection)"
        elif w_dir in ['S', 'SW'] and temp > 70:
            front_verdict = "Warm Frontal Incursion Active"
            wind_shift_alert = "Veering shift to Southern quadrant (Warm Air Advection)"

        if precip > 0 or humidity > 85:
            precip_potential = "High Probability (Ongoing or Imminent Downpour)"
        elif 70 <= humidity <= 85 and pressure < 1008:
            precip_potential = "Moderate / Developing Risk (Clouds Accumulating)"

        current_month = datetime.utcnow().month
        if current_month in [12, 1, 2]:
            season_name = "Winter"
        elif current_month in [3, 4, 5]:
            season_name = "Spring"
        elif current_month in [6, 7, 8]:
            season_name = "Summer"
        else:
            season_name = "Autumn"

        if moon_phase == 0 or moon_phase == 1:
            moon_label = "New Moon (Peak Solunar Feeding Period)"
            lunar_score_modifier = 25
        elif moon_phase == 0.5:
            moon_label = "Full Moon (Strong Nocturnal Feeding Activity)"
            lunar_score_modifier = 20
        elif 0.22 <= moon_phase <= 0.28 or 0.72 <= moon_phase <= 0.78:
            moon_label = "Quarter Moon (Moderate Solunar Activity)"
            lunar_score_modifier = 10
        else:
            moon_label = "Crescent / Gibbous Transition Phase"
            lunar_score_modifier = 5

        fish_score = 40 + lunar_score_modifier
        tactical_tip = f"Analyzing conditions for {target_species}."

        if target_species == "Bass":
            if "Falling" in barometer_trend or "Active" in front_verdict:
                fish_score += 25
                tactical_tip = "Barometer dropping! Bass are aggressively feeding ahead of the front. Run fast moving horizontal lures."
            elif pressure > 1020:
                fish_score -= 15
                tactical_tip = "Post-frontal high pressure slows down Bass. Slow down and drop finesse plastics tight to structural wood or weeds."
            else:
                tactical_tip = "Stable atmospheric criteria. Bass will mirror typical seasonal patterns along primary drop-offs."
            
            if temp > 82 or temp < 50:
                fish_score -= 10
                tactical_tip += " Thermal stress detected. Look for thermal protection boundaries or deep secondary holes."

        elif target_species == "Trout":
            if 50 <= temp <= 65:
                fish_score += 20
                tactical_tip = "Optimal cool oxygenated water window for Trout. Streamer and insect hatch imitation patterns will excel."
            elif temp > 70:
                fish_score -= 25
                tactical_tip = "Dangerously warm water conditions for Trout. Target deep oxygenated lake channels or spring-fed inputs."
            else:
                tactical_tip = "Cold winter trout parameters. Slow down drifts across slow deep pool bottoms."
                
            if w_speed > 12:
                fish_score -= 5

        elif target_species == "Catfish":
            if humidity > 75 or precip > 0:
                fish_score += 20
                tactical_tip = "High atmospheric humidity and rain trigger heavy Catfish movements. Focus efforts on shallow mudflats or river inlets."
            else:
                tactical_tip = "Standard pressure bounds. Catfish remain active along primary muddy creek channels and structures."
                
            if pressure < 1005:
                fish_score += 10

        final_fishing_score = max(5, min(98, fish_score))
        
        if final_fishing_score >= 75:
            fishing_verdict = f"EXCELLENT ({target_species} Prime Feeding Window)"
        elif final_fishing_score >= 50:
            fishing_verdict = f"GOOD (Consistent {target_species} Activity)"
        else:
            fishing_verdict = f"TOUGH (Highly Precise {target_species} Presentation Needed)"

        return jsonify({
            "success": True,
            "city": city,
            "target_species": target_species,
            "metrics": {
                "temp": temp,
                "pressure": pressure,
                "precip": precip,
                "w_speed": w_speed,
                "w_dir": w_dir,
                "humidity": humidity
            },
            "predictions": {
                "front": front_verdict,
                "wind": wind_shift_alert,
                "precip_risk": precip_potential,
                "baro_trend": barometer_trend
            },
            "angling_forecast": {
                "score": final_fishing_score,
                "verdict": fishing_verdict,
                "season": season_name,
                "lunar": moon_label,
                "strategy": tactical_tip
            },
            "history": history_list
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Predictive Core Error: {str(e)}"}), 500
