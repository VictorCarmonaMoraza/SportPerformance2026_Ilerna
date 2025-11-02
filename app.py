import io

from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from config.settings import settings
from flask_cors import CORS

from routes.auth.auth_routes import auth_bp
from routes.register.register_routes import register_bp
from routes.user.user_route import user_bp
import json
import os

# 🔹 Rutas absolutas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ⚡ Crear la app especificando la carpeta estatica
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
CORS(app)

# 👇 Verifica que el JSON se pueda abrir en UTF-8
swagger_path = os.path.join(os.path.dirname(__file__), "static", "swagger.json")
try:
    with io.open(swagger_path, "r", encoding="utf-8") as f:
        json.load(f)
except Exception as e:
    print("⚠️ Error al leer swagger.json:", e)

# 🔹 Registrar blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(register_bp)

# 🔹 Configurar Swagger
SWAGGER_URL = settings.SWAGGER_URL
API_URL = settings.API_URL

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": settings.APP_NAME}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Redireccion principal
@app.route("/")
def index():
    return redirect(SWAGGER_URL)


'''if __name__ == "__main__":
    print("📂 BASE_DIR:", BASE_DIR)
    print("📁 STATIC_DIR:", STATIC_DIR)
    print("🌍 Swagger UI → http://127.0.0.1:8000/swagger")
    print("📄 JSON directo → http://127.0.0.1:8000/static/swagger.json")
    app.run(host="0.0.0.0", port=8000, debug=True)'''

if __name__ == "__main__":
    print("🔥 Ejecutando Flask en modo debug sin reloader...")
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)
