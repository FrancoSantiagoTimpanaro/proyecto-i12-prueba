from flask import Flask
from app.extensions import db, migrate
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(main_bp)

    return app
