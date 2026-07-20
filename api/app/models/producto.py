from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class CategoriaProducto(str, enum.Enum):
    bebidas = "bebidas"
    comidas = "comidas"
    postres = "postres"
    otros = "otros"


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria = Column(Enum(CategoriaProducto), nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    items = relationship("Item", back_populates="producto")
