from fastapi import FastAPI
from app.routers import mesas, pedidos, productos

app = FastAPI(title="POS Cafetería", version="0.1.0")

app.include_router(mesas.router)
app.include_router(pedidos.router)
app.include_router(productos.router)

@app.get("/health")
def health():
    return {"status": "ok"}