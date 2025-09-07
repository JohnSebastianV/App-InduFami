from models import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(30), unique=True, nullable=False)
    pidio = db.Column(db.Boolean, default=False)

    reservas = db.relationship("Reserva", backref="usuario", lazy=True)

    def __repr__(self):
        return f"<User {self.nombre} - {self.cedula} - {self.rol}>"
