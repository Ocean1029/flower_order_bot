from flask import Blueprint, jsonify
from services.stats_service import get_stats

api_stats_bp = Blueprint('api_stats', __name__)

@api_stats_bp.route("/api/stats", methods=["GET"])
def get_stats_api():
    stats = get_stats()
    return jsonify(stats)
