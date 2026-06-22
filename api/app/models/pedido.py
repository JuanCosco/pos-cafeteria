from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class EstadoPedido(str, enum.Enum):
    abierto = "abierto"
    cerrado = "cerrado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.abierto, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    mesa = relationship("Mesa", back_populates="pedidos")
    items = relationship("Item", back_populates="pedido")