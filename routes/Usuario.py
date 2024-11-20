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

@router.post("/", response_model=Usuario)
async def create_usuario(usuario: Usuario):
    result = await db["usuarios"].insert_one(usuario.model_dump(by_alias=True))
    usuario.id = str(result.inserted_id)
    return usuario

@router.get("/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: str):
    usuario = await db["usuarios"].find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=Usuario)
async def update_usuario(usuario_id: str, usuario: Usuario):
    result = await db["usuarios"].update_one(
        {"_id": ObjectId(usuario_id)}, {"$set": usuario.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.id = usuario_id
    return usuario

@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: str):
    result = await db["usuarios"].delete_one({"_id": ObjectId(usuario_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}

#Buscar usuario por email y contraseña
@router.get("/login/{email}/{password}", response_model=Usuario)
async def get_usuario_by_email(email: str, password: str):
    usuario = await db["usuarios"].find_one({"email": email, "password": password})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
