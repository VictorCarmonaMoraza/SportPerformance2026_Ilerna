import os

def find_non_utf8_files(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".py", ".json", ".txt", ".md")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        f.read()
                except UnicodeDecodeError as e:
                    print(f"❌ Archivo con error de codificación: {path}")
                    print(f"   → {e}\n")

print("🔍 Buscando archivos no UTF-8...")
find_non_utf8_files(os.getcwd())
print("✅ Revisión terminada.")
