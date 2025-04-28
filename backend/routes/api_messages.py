from flask import Blueprint, jsonify
from services.message_service import get_latest_messages

api_messages_bp = Blueprint('api_messages', __name__)

@api_messages_bp.route("/api/messages", methods=["GET"])
def get_messages():
    messages = get_latest_messages()
    return jsonify({"messages": messages})
