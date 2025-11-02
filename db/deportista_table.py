from sqlalchemy import Column, Integer, ForeignKey, String

from db.base import Base


class Deportista(Base):
    __tablename__ = "deportistas"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("public.usuarios.id", ondelete="CASCADE"))
    nombre = Column(String(100))
    edad = Column(Integer)
    disciplina_deportiva = Column(String(100))
    nacionalidad = Column(String(100))
    telefono = Column(String(20))