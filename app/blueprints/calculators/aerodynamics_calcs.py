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
 
Aerodynamics = Blueprint('aero_bp', __name__, template_folder='../templates')

class AeroCalculators:
    @staticmethod
    def get_num(key):
        val = data.get(key)
        if val is None or val == "":
            return 0.0
        return float(val)
      
    def run_logic(cid, step, data):
        global db 
