def setup_routes(app):
    @app.route("/health")
    def health():
        return "OK", 200

