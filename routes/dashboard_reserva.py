from flask import Blueprint, flash, redirect, render_template, request, jsonify, session, url_for
from app import db
from models.dia import Dia
from models.plato import Plato
from models.reserva import Reserva
from models.user import User

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("usuario_id"):
        return redirect(url_for("auth.login"))

    nombre = session.get("usuario_nombre", "Usuario")
    dias = Dia.query.all()
    return render_template("dashboard.html", dias=dias, nombre=nombre)

@dashboard_bp.route("/get_platos", methods=["POST"])
def get_platos():
    data = request.json
    dias_ids = data.get("dias", [])

    platos = Plato.query.filter(Plato.dia_id.in_(dias_ids)).all()

    # Traemos los días seleccionados para saber sus nombres
    dias_map = {d.id: d.nombre for d in Dia.query.filter(Dia.id.in_(dias_ids)).all()}

    platos_data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "dia_id": p.dia_id,
            "dia_nombre": dias_map.get(p.dia_id, f"Día {p.dia_id}")
        }
        for p in platos
    ]

    return jsonify(platos_data)


@dashboard_bp.route("/guardar_reserva", methods=["POST"])
def guardar_reserva():
    data = request.json
    platos_ids = data.get("platos", [])

    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify({"success": False, "message": "Usuario no autenticado"}), 401

    try:
        # Obtener los platos seleccionados desde BD
        platos = Plato.query.filter(Plato.id.in_(platos_ids)).all()

        # Agrupar por día para verificar que no haya más de un plato por día
        platos_por_dia = {}
        for plato in platos:
            platos_por_dia.setdefault(plato.dia_id, []).append(plato)

        # Validación: si un día tiene más de un plato seleccionado, error
        for platos_dia in platos_por_dia.values():
            if len(platos_dia) > 1:
                return jsonify({
                    "success": False,
                    "message": f"Solo puedes seleccionar un plato para el día {platos_dia[0].dia.nombre}."
                }), 400


        # Guardar reservas
        for plato in platos:
            reserva = Reserva(usuario_id=usuario_id, plato_id=plato.id)
            db.session.add(reserva)

        # Actualizar usuario -> ya pidió
        usuario = User.query.get(usuario_id)
        usuario.pidio = True
        db.session.commit()

        # Cerrar sesión
        session.clear()

        return jsonify({
            "success": True,
            "message": "Reserva guardada con éxito. Tu sesión ha sido cerrada.",
            "redirect": url_for("auth.login")
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500







