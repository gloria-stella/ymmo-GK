"""
Application factory : crée et configure l'instance Flask.
Ce pattern facilite les tests et évite les imports circulaires.
"""
from flask import Flask, render_template
from .config import Config
from .extensions import db, login_manager


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import des modèles pour qu'ils soient connus de SQLAlchemy
    from . import models  # noqa: F401

    # Enregistrement des blueprints (routes)
    from .routes.auth import auth_bp
    from .routes.properties import properties_bp
    from .routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(analytics_bp)

    # Pages d'erreur accessibles
    @app.errorhandler(403)
    def forbidden(_):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/404.html"), 404

    return app