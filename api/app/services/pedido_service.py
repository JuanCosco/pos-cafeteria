from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.pedido import Pedido, EstadoPedido
from app.models.item import Item
from app.models.mesa import Mesa, EstadoMesa
from app.schemas.pedido import PedidoCreate, PedidoAddItem


def get_by_id(db: Session, pedido_id: int):
    return db.execute(
        select(Pedido).options(selectinload(Pedido.items)).where(Pedido.id == pedido_id)
    ).scalar_one_or_none()


def get_by_mesa(db: Session, mesa_id: int):
    return db.execute(
        select(Pedido)
        .options(selectinload(Pedido.items))
        .where(Pedido.mesa_id == mesa_id)
        .where(Pedido.estado == EstadoPedido.abierto)
    ).scalar_one_or_none()


def create(db: Session, data: PedidoCreate):
    # marcar mesa como ocupada
    mesa = db.get(Mesa, data.mesa_id)
    if not mesa:
        return None
    mesa.estado = EstadoMesa.ocupada

    pedido = Pedido(mesa_id=data.mesa_id)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return get_by_id(db, pedido.id)


def add_item(db: Session, pedido_id: int, data: PedidoAddItem):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        return None
    item = Item(
        pedido_id=pedido_id,
        nombre=data.nombre,
        precio_unitario=data.precio_unitario,
        cantidad=data.cantidad,
        comensal=data.comensal,
        es_compartido=data.es_compartido,
    )
    db.add(item)
    db.commit()
    return get_by_id(db, pedido_id)


def remove_item(db: Session, pedido_id: int, item_id: int):
    item = db.get(Item, item_id)
    if not item or item.pedido_id != pedido_id:
        return None
    db.delete(item)
    db.commit()
    return get_by_id(db, pedido_id)


def cerrar(db: Session, pedido_id: int):
    from sqlalchemy.sql import func

    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        return None
    pedido.estado = EstadoPedido.cerrado
    pedido.closed_at = func.now()

    # marcar mesa como libre
    mesa = db.get(Mesa, pedido.mesa_id)
    if mesa:
        mesa.estado = EstadoMesa.libre

    db.commit()
    return get_by_id(db, pedido_id)
