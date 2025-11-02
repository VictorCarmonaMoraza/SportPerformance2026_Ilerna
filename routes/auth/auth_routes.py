from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import check_password_hash

from auth.token_manager import generar_token
from config.config_bd import engine


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login de usuario y retorno del token + datos del deportista"""
    data = request.get_json()
    nameuser = data.get("nameuser")
    password = data.get("password")

    try:
        with engine.connect() as conn:
            user = conn.execute(
                text("SELECT * FROM usuarios WHERE nameuser = :nameuser"),
                {"nameuser": nameuser}
            ).mappings().first()

            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if not check_password_hash(user["passwordhash"], password):
                return jsonify({"error": "Contraseña incorrecta"}), 401

            # Traer datos del deportista
            deportista = conn.execute(
                text("""
                    SELECT id, nombre, edad, disciplina_deportiva, nacionalidad, telefono
                    FROM deportistas
                    WHERE usuario_id = :id
                """),
                {"id": user["id"]}
            ).mappings().first()

            # Convertir también deportista a dict
            deportista = dict(deportista) if deportista else {}

            token = generar_token(user["id"], user["rol"])

            return jsonify({
                "status": 200,
                "message": "Login correcto",
                "token": token,
                "usuario": {
                    "id": user["id"],
                    "nameuser": user["nameuser"],
                    "email": user["email"],
                    "rol": user["rol"]
                },
                "deportista": deportista or {}
            }), 200

    except Exception as e:
        print("❌ ERROR EN LOGIN:", e)
        return jsonify({"error": str(e)}), 500
