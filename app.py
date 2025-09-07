from flask import Flask
from config import Config
from models import db  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)

    with app.app_context():
       
        from models.user import User
        from models.dia import Dia
        from models.plato import Plato
        from models.reserva import Reserva

        db.create_all()

        
        from routes.auth import auth_bp
        from routes.dashboard_reserva import dashboard_bp
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(auth_bp)

    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


