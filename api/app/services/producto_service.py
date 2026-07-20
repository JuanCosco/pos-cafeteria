from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.producto import Producto, CategoriaProducto
from app.schemas.producto import ProductoCreate, ProductoUpdate


def get_all(db: Session, solo_disponibles: bool = False):
    query = select(Producto)
    if solo_disponibles:
        query = query.where(Producto.disponible == True)
    return db.execute(query).scalars().all()


def get_by_id(db: Session, producto_id: int):
    return db.get(Producto, producto_id)


def get_by_categoria(db: Session, categoria: CategoriaProducto):
    return (
        db.execute(
            select(Producto)
            .where(Producto.categoria == categoria)
            .where(Producto.disponible == True)
        )
        .scalars()
        .all()
    )


def create(db: Session, data: ProductoCreate):
    producto = Producto(**data.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def update(db: Session, producto_id: int, data: ProductoUpdate):
    producto = db.get(Producto, producto_id)
    if not producto:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(producto, field, value)
    db.commit()
    db.refresh(producto)
    return producto


def toggle_disponible(db: Session, producto_id: int):
    producto = db.get(Producto, producto_id)
    if not producto:
        return None
    producto.disponible = not producto.disponible
    db.commit()
    db.refresh(producto)
    return producto
