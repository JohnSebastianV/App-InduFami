from flask import Flask
from config import Config
from models import db   # Importa el db global

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la BD
    db.init_app(app)

    with app.app_context():
        # Importa los modelos aquí (así no hay referencias circulares)
        from models.user import User
        from models.dia import Dia
        from models.plato import Plato
        from models.reserva import Reserva

        db.create_all()

        # Importa y registra las rutas
        from routes.auth import auth_bp
        from routes.dashboard_reserva import dashboard_bp
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

