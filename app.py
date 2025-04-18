import os
from flask import Flask
from routes import health
from routes import linebot
from routes import index

app = Flask(__name__)

health.setup_routes(app)
linebot.setup_routes(app)
index.setup_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # render deployment default port
    app.run(host="0.0.0.0", port=port, debug=True)
