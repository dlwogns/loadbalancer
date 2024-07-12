from .reverseProxy import bp as my_routes_bp

def init_routes(app):
    app.register_blueprint(my_routes_bp)