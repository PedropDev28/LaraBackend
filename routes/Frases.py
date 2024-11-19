from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Frases import Frases

router = APIRouter()

@router.get("/", response_model=List[Frases])
async def get_frases():
    frases = await db["frases"].find().to_list(100)
    return frases

@router.post("/", response_model=Frases)
async def create_frases(frases: Frases):
    result = await db["frases"].insert_one(frases.model_dump(by_alias=True))
    frases.id = str(result.inserted_id)
    return frases

@router.get("/{frases_id}", response_model=Frases)
async def get_frases(frases_id: str):
    frases = await db["frases"].find_one({"_id": ObjectId(frases_id)})
    if not frases:
        raise HTTPException(status_code=404, detail="Frase no encontrada")
    return frases

@router.put("/{frases_id}", response_model=Frases)
async def update_frases(frases_id: str, frases: Frases):
    result = await db["frases"].update_one(
        {"_id": ObjectId(frases_id)}, {"$set": frases.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Frase no encontrada")
    frases.id = frases_id
    return frases

@router.delete("/{frases_id}")
async def delete_frases(frases_id: str):
    result = await db["frases"].delete_one({"_id": ObjectId(frases_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Frase no encontrada")
    return {"message": "Frase eliminada"}
