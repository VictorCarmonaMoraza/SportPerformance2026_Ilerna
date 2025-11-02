from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base
from datetime import datetime

class Users(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nameuser = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    passwordhash = Column(String(255), nullable=False)
    rol = Column(String(50), default='deportista')
    creado_en = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nameuser": self.nameuser,
            "email": self.email,
            "rol": self.rol,
            "creado_en": str(self.creado_en)
        }
