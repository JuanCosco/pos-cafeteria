from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.grupo_pago import GrupoPago
from app.models.item import Item
from app.models.pedido import Pedido


def crear_grupos(db: Session, pedido_id: int, nombres: list[str]):
    """Crea los grupos de pago para un pedido."""
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        return None

    # eliminar grupos anteriores si existían
    grupos_existentes = (
        db.execute(select(GrupoPago).where(GrupoPago.pedido_id == pedido_id))
        .scalars()
        .all()
    )
    for g in grupos_existentes:
        db.delete(g)

    grupos = []
    for nombre in nombres:
        grupo = GrupoPago(pedido_id=pedido_id, nombre=nombre)
        db.add(grupo)
        grupos.append(grupo)

    db.commit()
    for g in grupos:
        db.refresh(g)
    return grupos


def asignar_item(db: Session, pedido_id: int, item_id: int, grupo_pago_id: int):
    """Asigna un item a un grupo de pago."""
    item = db.get(Item, item_id)
    if not item or item.pedido_id != pedido_id:
        return None

    grupo = db.get(GrupoPago, grupo_pago_id)
    if not grupo or grupo.pedido_id != pedido_id:
        return None

    item.grupo_pago_id = grupo_pago_id
    db.commit()
    db.refresh(item)
    return item


def dividir(db: Session, pedido_id: int):
    """Calcula cuánto paga cada grupo."""
    grupos = (
        db.execute(
            select(GrupoPago)
            .options(selectinload(GrupoPago.items))
            .where(GrupoPago.pedido_id == pedido_id)
        )
        .scalars()
        .all()
    )

    if not grupos:
        return None

    # items compartidos — se dividen entre todos los grupos
    items_compartidos = (
        db.execute(
            select(Item)
            .where(Item.pedido_id == pedido_id)
            .where(Item.es_compartido == True)
        )
        .scalars()
        .all()
    )

    total_compartido = sum(
        float(i.precio_unitario) * i.cantidad for i in items_compartidos
    )
    parte_compartida = round(total_compartido / len(grupos), 2) if grupos else 0

    # items sin asignar a ningún grupo
    items_sin_asignar = (
        db.execute(
            select(Item)
            .where(Item.pedido_id == pedido_id)
            .where(Item.grupo_pago_id == None)
            .where(Item.es_compartido == False)
        )
        .scalars()
        .all()
    )

    resultado = []
    for grupo in grupos:
        items_propios = [i for i in grupo.items]
        total_propio = sum(float(i.precio_unitario) * i.cantidad for i in items_propios)
        resultado.append(
            {
                "grupo_id": grupo.id,
                "nombre": grupo.nombre,
                "items": [
                    {
                        "nombre": i.nombre,
                        "cantidad": i.cantidad,
                        "subtotal": round(float(i.precio_unitario) * i.cantidad, 2),
                    }
                    for i in items_propios
                ],
                "total_propio": round(total_propio, 2),
                "parte_compartida": parte_compartida,
                "total_a_pagar": round(total_propio + parte_compartida, 2),
            }
        )

    return {
        "pedido_id": pedido_id,
        "grupos": resultado,
        "compartido": {
            "items": [
                {
                    "nombre": i.nombre,
                    "cantidad": i.cantidad,
                    "subtotal": round(float(i.precio_unitario) * i.cantidad, 2),
                }
                for i in items_compartidos
            ],
            "total": round(total_compartido, 2),
            "dividido_entre": len(grupos),
        },
        "sin_asignar": [
            {"id": i.id, "nombre": i.nombre, "cantidad": i.cantidad}
            for i in items_sin_asignar
        ],
    }
