import math
from flask import Flask, request, jsonify, Blueprint

Vectors = Blueprint('vectors_bp', __name__)

class Vectors:
