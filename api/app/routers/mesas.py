from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.mesa import MesaCreate, MesaUpdate, MesaResponse
from app.services import mesa_service

router = APIRouter(prefix="/mesas", tags=["mesas"])


@router.get("/", response_model=List[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    return mesa_service.get_all(db)


@router.get("/{mesa_id}", response_model=MesaResponse)
def obtener_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = mesa_service.get_by_id(db, mesa_id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.post("/", response_model=MesaResponse, status_code=201)
def crear_mesa(data: MesaCreate, db: Session = Depends(get_db)):
    return mesa_service.create(db, data)


@router.patch("/{mesa_id}/estado", response_model=MesaResponse)
def actualizar_estado(mesa_id: int, data: MesaUpdate, db: Session = Depends(get_db)):
    mesa = mesa_service.update_estado(db, mesa_id, data)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa


@router.delete("/{mesa_id}", response_model=MesaResponse)
def eliminar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = mesa_service.delete(db, mesa_id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa
