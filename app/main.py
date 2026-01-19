from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.branches import router as branches_router
from app.routers.warehouses import router as warehouses_router
from app.routers.materials import router as materials_router

app = FastAPI()

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(branches_router)
app.include_router(warehouses_router)
app.include_router(materials_router)

@app.get("/")
async def root():
    return {"status": "OK"}