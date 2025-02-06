# routes/usuarios.py
from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Usuario import Usuario

router = APIRouter()

@router.get("/", response_model=List[Usuario])
async def get_usuarios():
    usuarios = await db["usuarios"].find().to_list(100)
    return usuarios

@router.get("/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: str):
    usuario = await db["usuarios"].find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: str):
    result = await db["usuarios"].delete_one({"_id": ObjectId(usuario_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}

@router.get("/by_username/{username}", response_model=Usuario)
async def get_usuario_by_username(username: str):
    usuario = await db["usuarios"].find_one({"username": username})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario