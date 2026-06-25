from sqlalchemy.orm import Session
from app.models.mesa import Mesa, EstadoMesa
from app.schemas.mesa import MesaCreate, MesaUpdate


def get_all(db: Session):
    return db.execute(__import__("sqlalchemy").select(Mesa)).scalars().all()


def get_by_id(db: Session, mesa_id: int):
    return db.get(Mesa, mesa_id)


def create(db: Session, data: MesaCreate):
    mesa = Mesa(numero=data.numero)
    db.add(mesa)
    db.commit()
    db.refresh(mesa)
    return mesa


def update_estado(db: Session, mesa_id: int, data: MesaUpdate):
    mesa = db.get(Mesa, mesa_id)
    if not mesa:
        return None
    mesa.estado = data.estado
    db.commit()
    db.refresh(mesa)
    return mesa


def delete(db: Session, mesa_id: int):
    mesa = db.get(Mesa, mesa_id)
    if not mesa:
        return None
    db.delete(mesa)
    db.commit()
    return mesa
