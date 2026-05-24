import math
from flask import Flask, request, jsonify, Blueprint

Interpolation = Blueprint('interpolation_bp', __name__)

class Interpolation:
