from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Sylabus import Sylabus

router = APIRouter()

@router.get("/", response_model=List[Sylabus])
async def get_sylabus():
    sylabus = await db["sylabus"].find().to_list(100)
    return sylabus

@router.post("/", response_model=Sylabus)
async def create_sylabus(sylabus: Sylabus):
    result = await db["sylabus"].insert_one(sylabus.model_dump(by_alias=True))
    sylabus.id = str(result.inserted_id)
    return sylabus

@router.get("/{sylabus_id}", response_model=Sylabus)
async def get_sylabus(sylabus_id: str):
    sylabus = await db["sylabus"].find_one({"_id": ObjectId(sylabus_id)})
    if not sylabus:
        raise HTTPException(status_code=404, detail="Sylabus no encontrado")
    return sylabus

@router.put("/{sylabus_id}", response_model=Sylabus)
async def update_sylabus(sylabus_id: str, sylabus: Sylabus):
    result = await db["sylabus"].update_one(
        {"_id": ObjectId(sylabus_id)}, {"$set": sylabus.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sylabus no encontrado")
    sylabus.id = sylabus_id
    return sylabus

@router.delete("/{sylabus_id}")
async def delete_sylabus(sylabus_id: str):
    result = await db["sylabus"].delete_one({"_id": ObjectId(sylabus_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sylabus no encontrado")
    return {"message": "Sylabus eliminado"}