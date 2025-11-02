from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from config.config_bd import engine

register_bp = Blueprint("register_bp", __name__, url_prefix="/api")

@register_bp.route("/register", methods=["POST"])
def register_user():
    """
    Crea un nuevo usuario en la base de datos.
    Requiere: nameuser, email, password, rol (opcional)
    """
    data = request.get_json()

    nameuser = data.get("nameuser")
    email = data.get("email")
    password = data.get("password")
    rol = data.get("rol", "deportista")  # por defecto 'deportista'

    if not nameuser or not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        # Generar hash seguro de la contraseña
        passwordhash = generate_password_hash(password)

        with engine.connect() as conn:
            # Verificar si ya existe el usuario o email
            existing_user = conn.execute(
                text("SELECT id FROM usuarios WHERE nameuser = :nameuser OR email = :email"),
                {"nameuser": nameuser, "email": email}
            ).fetchone()

            if existing_user:
                return jsonify({"error": "El usuario o email ya existen"}), 409

            # Insertar nuevo usuario
            conn.execute(
                text("""
                    INSERT INTO usuarios (nameuser, email, passwordhash, rol)
                    VALUES (:nameuser, :email, :passwordhash, :rol)
                """),
                {
                    "nameuser": nameuser,
                    "email": email,
                    "passwordhash": passwordhash,
                    "rol": rol
                }
            )
            conn.commit()

        return jsonify({
            "status": 201,
            "message": "Usuario creado correctamente",
            "data": {
                "nameuser": nameuser,
                "email": email,
                "rol": rol
            }
        }), 201

    except Exception as e:
        print("❌ ERROR al registrar usuario:", e)
        return jsonify({"error": str(e)}), 500
