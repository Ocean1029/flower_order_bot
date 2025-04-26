import os
from flask import Flask
from routes.health import health_bp
from routes.linebot import linebot_bp
from routes.index import index_bp

app = Flask(__name__)

app.register_blueprint(health_bp)
app.register_blueprint(linebot_bp)
app.register_blueprint(index_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # render deployment default port
    app.run(host="0.0.0.0", port=port, debug=True)
