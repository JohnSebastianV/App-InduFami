from models import db

class Dia(db.Model):
    __tablename__ = "dias"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación con Plato
    platos = db.relationship("Plato", back_populates="dia")

    def __repr__(self):
        return f"<Dia {self.nombre}>"

