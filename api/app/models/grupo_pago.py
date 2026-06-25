from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class GrupoPago(Base):
    __tablename__ = "grupos_pago"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    nombre = Column(String(50), nullable=False)  # "Grupo 1", "Pareja", etc.

    pedido = relationship("Pedido", back_populates="grupos_pago")
    items = relationship("Item", back_populates="grupo_pago")
