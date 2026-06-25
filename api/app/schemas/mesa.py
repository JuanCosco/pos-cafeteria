from pydantic import BaseModel
from app.models.mesa import EstadoMesa


class MesaCreate(BaseModel):
    numero: int


class MesaUpdate(BaseModel):
    estado: EstadoMesa


class MesaResponse(BaseModel):  ## Sale en la respuesta de la API
    id: int
    numero: int
    estado: EstadoMesa

    model_config = {"from_attributes": True}
