from flask import Blueprint, jsonify
from sqlalchemy import text
from config.config_bd import engine
from shared.domain.models.user_model import Users

user_bp = Blueprint("user_bp", __name__, url_prefix="/api")


@user_bp.route("/usuarios", methods=["GET"])
def get_usuarios():
    """Obtiene todos los usuarios de la tabla 'usuarios'"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT id, nameuser, email, passwordhash, rol, creado_en
                    FROM usuarios
                """)
            )

            usuarios = [
                Users(
                    id=row.id,
                    nameuser=row.nameuser,
                    email=row.email,
                    passwordhash=row.passwordhash,
                    rol=row.rol,
                    creado_en=row.creado_en
                ).to_dict()
                for row in result
            ]

        return jsonify({
            "status": 200,
            "message": "Usuarios obtenidos correctamente",
            "data": usuarios
        }), 200

    except Exception as e:
        print("❌ ERROR AL CONSULTAR USUARIOS:", e)
        return jsonify({"error": str(e)}), 500
