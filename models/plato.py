from models import db

class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia_id = db.Column(db.Integer, db.ForeignKey("dias.id"), nullable=False)

    dia = db.relationship("Dia", back_populates="platos")

    semana = db.Column(db.String(10), nullable=False)  

    reservas = db.relationship("Reserva", backref="plato", lazy=True)
    
    def __repr__(self):
        return f"<Plato {self.nombre} - Dia {self.dia_id} - Semana {self.semana}>"



