from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    es_compartido = Column(Boolean, default=False, nullable=False)
    grupo_pago_id = Column(Integer, ForeignKey("grupos_pago.id"), nullable=True)

    pedido = relationship("Pedido", back_populates="items")
    grupo_pago = relationship("GrupoPago", back_populates="items")
    producto = relationship("Producto", back_populates="items")