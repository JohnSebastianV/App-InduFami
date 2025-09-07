from models import db

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)

    def __repr__(self):
        return f"<Reserva Usuario={self.usuario_id}, Dia={self.dia_id}, Plato={self.plato_id}>"
