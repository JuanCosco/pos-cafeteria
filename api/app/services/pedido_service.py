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


## Dividir cuenta
def dividir_cuenta(db: Session, pedido_id: int):
    pedido = get_by_id(db, pedido_id)
    if not pedido:
        return None

    compartidos = [i for i in pedido.items if i.es_compartido]
    individuales = [i for i in pedido.items if not i.es_compartido]

    # comensales únicos que tienen items individuales
    comensales = list({i.comensal for i in individuales if i.comensal})

    total_compartido = sum(float(i.precio_unitario) * i.cantidad for i in compartidos)
    parte_compartida = total_compartido / len(comensales) if comensales else 0

    resultado = {}
    for comensal in comensales:
        items_propios = [i for i in individuales if i.comensal == comensal]
        total_propio = sum(float(i.precio_unitario) * i.cantidad for i in items_propios)
        resultado[comensal] = {
            "items": [
                {
                    "nombre": i.nombre,
                    "cantidad": i.cantidad,
                    "subtotal": float(i.precio_unitario) * i.cantidad,
                }
                for i in items_propios
            ],
            "total_propio": round(total_propio, 2),
            "parte_compartida": round(parte_compartida, 2),
            "total_a_pagar": round(total_propio + parte_compartida, 2),
        }

    # items sin asignar
    sin_asignar = [i for i in individuales if not i.comensal]

    return {
        "pedido_id": pedido_id,
        "comensales": resultado,
        "compartido": {
            "items": [
                {
                    "nombre": i.nombre,
                    "cantidad": i.cantidad,
                    "subtotal": float(i.precio_unitario) * i.cantidad,
                }
                for i in compartidos
            ],
            "total": round(total_compartido, 2),
            "dividido_entre": len(comensales),
        },
        "sin_asignar": [
            {"nombre": i.nombre, "cantidad": i.cantidad} for i in sin_asignar
        ],
    }
