import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

# Clave secreta usada para firmar los tokens
SECRET_KEY = "super_clave_segura"

# ==========================================================
# 🧩 Función para generar token JWT
# ==========================================================
def generar_token(user_id, rol):
    """
    Genera un token JWT con ID de usuario, rol y expiración (3 horas)
    """
    payload = {
        "user_id": user_id,
        "rol": rol,
        "exp": datetime.utcnow() + timedelta(hours=3)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # PyJWT >= 2.x devuelve un string directamente, no hace falta .decode()
    return token


# ==========================================================
# 🧠 Decorador para verificar token JWT en rutas protegidas
# ==========================================================
def verificar_token(f):
    """
    Decorador para verificar tokens JWT en endpoints protegidos.
    Requiere un header: Authorization: Bearer <token>
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # Validar que el header exista y tenga formato correcto
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token no proporcionado"}), 401

        token = auth_header.split(" ")[1]

        try:
            # Decodificar el token y obtener los datos
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Guardar datos del usuario autenticado (puedes pasarlos a la vista)
            request.user = decoded

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        # Ejecutar la función original
        return f(*args, **kwargs)

    return wrapper
