def setup_routes(app):
    @app.route("/health")
    def health():
        return "OK", 200

    @app.route("/")
    def index():
        return "Hello, this is the LINE bot server!", 200
