from sqlalchemy import Column, Integer, String, Date, Float
from db.base import Base


class User(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100))
    ciudad = Column(String(100))
    pesoactual = Column(Float)
    tipoentrenamiento = Column(String(100))
