import os
from flask import Flask
from flask_cors import CORS
from routes.health import health_bp
from routes.linebot import linebot_bp
from routes.index import index_bp
from routes.api_orders import api_orders_bp
from routes.api_messages import api_messages_bp
from routes.api_stats import api_stats_bp


app = Flask(__name__)

CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(linebot_bp)
app.register_blueprint(index_bp)
app.register_blueprint(api_orders_bp)
app.register_blueprint(api_messages_bp)
app.register_blueprint(api_stats_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # render deployment default port
    app.run(host="0.0.0.0", port=port, debug=True)
