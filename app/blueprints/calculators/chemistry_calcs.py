"""
CREATE:
Following -> the same structure as fishing & hydrology calculators
"""

import math
import requests
from datetime import datetime
from urllib.parse import quote
from app.models.user import User, db
from app.models.weather_log import ApiWeatherLog
from app.models.weather_log_summary import WeatherLog
 from flask import Blueprint, render_template, request, jsonify
 
Chemistry = Blueprint('chemistry_bp', __name__, template_folder='../templates')

@chemistry_bp.route('/chemistry-calc', methods=['GET'])
def chemistry_page():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    return render_template('calculators/chemistry_calcs.html', user=user)

@chemistry_bp.route('/api/chemistry/execute', methods=['POST'])
def execute_chemistry_calc():
    if 'user_id' not in session: 
        return jsonify({"error": "Unauthorized"}), 401
        
    payload = request.get_json() or {}
    cid = str(payload.get('cid', '1'))       
    step = str(payload.get('step', '1.1'))     
    data = payload.get('data', {}) 

class Chemistry:
    @staticmethod
    def get_num(key):
        val = data.get(key)
        if val is None or val == "":
            return 0.0
        return float(val)
      
    def run_logic(cid, step, data):
        global db 

