# models/usuario_model.py
from sqlalchemy import Column, Integer, String, Date, Float
from shared.domain.models.base import Base


class Deportistas(Base):
    __tablename__ = "deportistas"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fechanacimiento = Column(Date, nullable=False)          # 🔹 cambiado
    email = Column(String(100))
    ciudad = Column(String(100))
    pesoactual = Column(Float)                              # 🔹 cambiado
    tipoentrenamiento = Column(String(100))                 # 🔹 cambiado

    def to_dict(self):
        """Convierte el objeto SQLAlchemy en diccionario JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fechanacimiento": str(self.fechanacimiento),  # 🔹 devuelto con guion para API
            "email": self.email,
            "ciudad": self.ciudad,
            "pesoactual": self.pesoactual,
            "tipoentrenamiento": self.tipoentrenamiento
        }
