from pydantic import BaseModel
from typing import Optional
from app.models.pedido import EstadoPedido


class ItemBase(BaseModel):
    nombre: str
    precio_unitario: float
    cantidad: int = 1
    comensal: Optional[str] = None
    es_compartido: bool = False


class ItemResponse(ItemBase):
    id: int
    pedido_id: int

    model_config = {"from_attributes": True}


class PedidoCreate(BaseModel):
    mesa_id: int


class PedidoAddItem(BaseModel):
    producto_id: int
    cantidad: int = 1
    es_compartido: bool = False


class PedidoResponse(BaseModel):
    id: int
    mesa_id: int
    estado: EstadoPedido
    items: list[ItemResponse] = []

    model_config = {"from_attributes": True}
