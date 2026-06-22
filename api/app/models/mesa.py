from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class EstadoMesa(str, enum.Enum):
    libre = "libre"
    ocupada = "ocupada"
    pidio_cuenta = "pidio_cuenta"


class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    estado = Column(Enum(EstadoMesa), default=EstadoMesa.libre, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pedidos = relationship("Pedido", back_populates="mesa")