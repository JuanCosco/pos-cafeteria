from pydantic import BaseModel
from typing import Optional
from app.models.producto import CategoriaProducto


class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    categoria: CategoriaProducto


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[CategoriaProducto] = None
    disponible: Optional[bool] = None


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    categoria: CategoriaProducto
    disponible: bool

    model_config = {"from_attributes": True}
