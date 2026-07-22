# POS Cafetería

Sistema de comandas interno para cafeterías pequeñas. Permite registrar pedidos por mesa y dividir la cuenta de múltiples formas al momento del cobro.

Construido como proyecto de portfolio para demostrar integración de un stack moderno con un problema de negocio real.

---

## Stack

| Capa          | Tecnología               |
| ------------- | ------------------------ |
| Backend       | FastAPI + Python 3.12    |
| ORM           | SQLAlchemy 2.0           |
| Migraciones   | Alembic                  |
| Base de datos | PostgreSQL 16            |
| Frontend      | Next.js 16 + TypeScript  |
| UI            | shadcn/ui + Tailwind CSS |
| Contenedores  | Docker + Docker Compose  |

---

## Funcionalidades

**Gestión de mesas**

- Vista en tiempo real del estado de cada mesa (libre, ocupada, pidió cuenta)
- Apertura automática de pedido al tocar una mesa libre
- Refresco automático cada 15 segundos

**Comandas**

- Carta organizada por categorías (bebidas, comidas, postres)
- Precios tomados de la base de datos con snapshot al momento del pedido
- Agregar y quitar items en tiempo real

**Cobro — tres modalidades**

- Cuenta única — total completo para un solo pago
- Partes iguales — divide el total entre N personas sin asignar platos
- Por grupos — asigna cada plato a un grupo de pago; los items compartidos se dividen proporcionalmente entre todos los grupos

---

## Estructura del proyecto
``` TEXT
pos-cafeteria/
├── api/ # FastAPI
│ ├── app/
│ │ ├── models/ # SQLAlchemy ORM
│ │ ├── schemas/ # Pydantic
│ │ ├── services/ # lógica de negocio
│ │ └── routers/ # endpoints
│ └── alembic/ # migraciones
├── frontend/ # Next.js
│ └── app/
│ └── mesas/ # vistas principales
└── docker-compose.yml

---
```
## Levantar el proyecto

**Requisitos**

- Docker y Docker Compose

**Pasos**

```bash
git clone https://github.com/JuanCosco/pos-cafeteria.git
cd pos-cafeteria
cp .env.example .env
docker compose up --build
```

| Servicio     | URL                        |
| ------------ | -------------------------- |
| Frontend     | http://localhost:3000      |
| API docs     | http://localhost:8000/docs |
| Adminer (DB) | http://localhost:8080      |

---

## Modelo de datos

productos → items ← pedidos → mesas
↑
grupos_pago

- `productos` — carta del local con precio y categoría
- `pedidos` — comanda activa de una mesa
- `items` — cada plato pedido con snapshot de nombre y precio
- `grupos_pago` — agrupaciones de pago creadas al momento del cobro
- `mesas` — estado en tiempo real de cada mesa

---

## Decisiones de diseño

**Snapshot de precio en items** — cuando el dueño actualiza el precio de un producto, los pedidos históricos no se modifican. Cada item guarda el precio exacto al momento en que fue pedido.

**División de cuenta al cobrar, no al pedir** — el mozo registra el pedido normalmente sin pensar en quién paga qué. La asignación por grupos ocurre solo si el cliente lo solicita al momento del cobro.

**Docker Compose con healthcheck** — el contenedor de la API espera que PostgreSQL esté listo antes de arrancar, evitando errores de conexión al levantar el stack.
