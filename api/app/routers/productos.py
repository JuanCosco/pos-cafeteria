from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.producto import CategoriaProducto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.services import producto_service

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(solo_disponibles: bool = False, db: Session = Depends(get_db)):
    return producto_service.get_all(db, solo_disponibles)


@router.get("/categoria/{categoria}", response_model=List[ProductoResponse])
def por_categoria(categoria: CategoriaProducto, db: Session = Depends(get_db)):
    return producto_service.get_by_categoria(db, categoria)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = producto_service.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    return producto_service.create(db, data)


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    producto = producto_service.update(db, producto_id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.patch("/{producto_id}/disponible", response_model=ProductoResponse)
def toggle_disponible(producto_id: int, db: Session = Depends(get_db)):
    producto = producto_service.toggle_disponible(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto