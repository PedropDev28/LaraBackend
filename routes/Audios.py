from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Audios import Audios

router = APIRouter()

@router.get("/", response_model=List[Audios])
async def get_audios():
    audios = await db["audios"].find().to_list(15000)
    return audios

@router.get("/five_less", response_model=List[Audios])
async def get_five_less_audios():
    pipeline = [
    {"$group": {"_id": "$texto.tag", "count": {"$sum": 1}}},
    {"$sort": {"count": 1}},
    {"$limit": 5}
    ]
    audios = await db["audios"].aggregate(pipeline).to_list(5)
    return audios

@router.get("/five_random", response_model=List[Audios])
async def get_five_random_audios():
    pipeline = [
    {"$sample": {"size": 5}}
    ]
    audios = await db["audios"].aggregate(pipeline).to_list(5)
    return audios

@router.post("/", response_model=Audios)
async def create_audios(audios: Audios):
    result = await db["audios"].insert_one(audios.dict(by_alias=True))
    audios.id = str(result.inserted_id)
    return audios

@router.get("/{audios_id}", response_model=Audios)
async def get_audios(audios_id: str):
    audios = await db["audios"].find_one({"_id": ObjectId(audios_id)})
    if not audios:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return audios

@router.put("/{audios_id}", response_model=Audios)
async def update_audios(audios_id: str, audios: Audios):
    result = await db["audios"].update_one(
        {"_id": ObjectId(audios_id)}, {"$set": audios.dict(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    audios.id = audios_id
    return audios

@router.delete("/{audios_id}")
async def delete_audios(audios_id: str):
    result = await db["audios"].delete_one({"_id": ObjectId(audios_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return {"message": "Audios eliminado"}