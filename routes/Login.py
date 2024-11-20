from fastapi import APIRouter, HTTPException
from db import db
from models.Login import Login

router = APIRouter()


@router.post("/")
async def login(login_data: Login):
    usuario = await db["usuarios"].find_one({"mail": login_data.email, "password": login_data.password})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"usuario": usuario}