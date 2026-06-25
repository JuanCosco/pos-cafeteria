from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoAddItem, PedidoResponse
from app.services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("/", response_model=PedidoResponse, status_code=201)
def crear_pedido(data: PedidoCreate, db: Session = Depends(get_db)):
    pedido = pedido_service.create(db, data)
    if not pedido:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return pedido


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.get_by_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.get("/mesa/{mesa_id}", response_model=PedidoResponse)
def pedido_activo_mesa(mesa_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.get_by_mesa(db, mesa_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="No hay pedido activo en esta mesa")
    return pedido


@router.post("/{pedido_id}/items", response_model=PedidoResponse)
def agregar_item(pedido_id: int, data: PedidoAddItem, db: Session = Depends(get_db)):
    pedido = pedido_service.add_item(db, pedido_id, data)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.delete("/{pedido_id}/items/{item_id}", response_model=PedidoResponse)
def eliminar_item(pedido_id: int, item_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.remove_item(db, pedido_id, item_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return pedido


@router.patch("/{pedido_id}/cerrar", response_model=PedidoResponse)
def cerrar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.cerrar(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.get("/{pedido_id}/dividir")
def dividir_cuenta(pedido_id: int, db: Session = Depends(get_db)):
    resultado = pedido_service.dividir_cuenta(db, pedido_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return resultado
