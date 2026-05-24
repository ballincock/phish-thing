import math
from flask import Flask, request, jsonify, Blueprint

Kurtosis = Blueprint('kurtosis_bp', __name__)

class Kurtosis:
