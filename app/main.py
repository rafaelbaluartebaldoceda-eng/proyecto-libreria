"""Punto de entrada principal para la API FastAPI del proyecto."""

from fastapi import FastAPI

from app.routers.clientes import router as clientes_router
from app.routers.libros import router as libros_router


app = FastAPI(
    title="Sistema de Gestion de Libreria API",
    version="3.0.0",
    description="API REST del proyecto de libreria.",
)


@app.get("/", tags=["Home"])
def home():
    """Retorna un mensaje simple para verificar que la API responde."""
    return {"message": "Bienvenido a la API de libreria"}


app.include_router(libros_router)
app.include_router(clientes_router)
