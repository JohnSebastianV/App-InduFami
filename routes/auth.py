from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cedula = request.form.get("cedula")

        usuario = User.query.filter_by(cedula=cedula).first()

        if usuario:
            if usuario.pidio:  # 👈 Nuevo control
                flash("Ya has hecho una reserva y no puedes ingresar nuevamente.", "error")
                return redirect(url_for("auth.login"))

            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre

            return redirect(url_for("dashboard_bp.dashboard"))
        else:
            flash("No existe esa cédula, intente de nuevo", "error")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))

