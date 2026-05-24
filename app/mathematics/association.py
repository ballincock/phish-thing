import math
from flask import Flask, request, jsonify, Blueprint

Association = Blueprint('association_bp', __name__)

class Association:
